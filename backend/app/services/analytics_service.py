from typing import List, Dict, Any
from app.core.database import get_collection
from pymongo import ASCENDING, DESCENDING

class AnalyticsService:
    async def get_crime_trends(self, district: str = None) -> Dict[str, Any]:
        """
        Get monthly crime trends (aggregated by month).
        """
        col = get_collection("crime_records")
        match_stage = {}
        if district:
            match_stage["district"] = {"$regex": f"^{district}$", "$options": "i"}

        pipeline = [
            {"$match": match_stage} if match_stage else {"$match": {}},
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$date"},
                        "month": {"$month": "$date"}
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "date": {
                        "$concat": [
                            {"$toString": "$_id.year"},
                            "-",
                            {"$cond": [
                                {"$lt": ["$_id.month", 10]},
                                {"$concat": ["0", {"$toString": "$_id.month"}]},
                                {"$toString": "$_id.month"}
                            ]}
                        ]
                    },
                    "count": 1
                }
            },
            {"$sort": {"date": 1}}
        ]
        
        cursor = col.aggregate(pipeline)
        results = await cursor.to_list(length=100)
        
        labels = [r["date"] for r in results]
        values = [r["count"] for r in results]
        
        return {
            "type": "line",
            "labels": labels,
            "values": values
        }

    async def get_crime_hotspots(self, district: str = None) -> List[Dict[str, Any]]:
        """
        Extract lat/long clusters with weights for GIS map display.
        """
        col = get_collection("crime_records")
        match_stage = {}
        if district:
            match_stage["district"] = {"$regex": f"^{district}$", "$options": "i"}

        pipeline = [
            {"$match": match_stage} if match_stage else {"$match": {}},
            {
                "$group": {
                    "_id": {
                        # Round to 3 decimal places to cluster coordinates (approx 100 meters resolution)
                        "lat": {"$round": ["$latitude", 3]},
                        "lon": {"$round": ["$longitude", 3]}
                    },
                    "count": {"$sum": 1},
                    "crime_types": {"$push": "$crime_type"},
                    "district": {"$first": "$district"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "latitude": "$_id.lat",
                    "longitude": "$_id.lon",
                    "weight": "$count",
                    "crime_type": {"$arrayElemAt": ["$crime_types", 0]},
                    "district": 1
                }
            },
            {"$sort": {"weight": -1}},
            {"$limit": 200}
        ]
        
        cursor = col.aggregate(pipeline)
        return await cursor.to_list(length=200)

    async def get_district_stats(self) -> Dict[str, Any]:
        """
        Get aggregated crime count by district.
        """
        col = get_collection("crime_records")
        pipeline = [
            {
                "$group": {
                    "_id": "$district",
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "district": "$_id",
                    "count": 1
                }
            },
            {"$sort": {"count": -1}}
        ]
        
        cursor = col.aggregate(pipeline)
        results = await cursor.to_list(length=100)
        
        labels = [r["district"] for r in results if r["district"]]
        values = [r["count"] for r in results if r["district"]]
        
        return {
            "type": "bar",
            "labels": labels,
            "values": values
        }

    async def get_crime_type_distribution(self, district: str = None) -> Dict[str, Any]:
        """
        Distribution of crimes by category/type.
        """
        col = get_collection("crime_records")
        match_stage = {}
        if district:
            match_stage["district"] = {"$regex": f"^{district}$", "$options": "i"}

        pipeline = [
            {"$match": match_stage} if match_stage else {"$match": {}},
            {
                "$group": {
                    "_id": "$crime_type",
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "crime_type": "$_id",
                    "count": 1
                }
            },
            {"$sort": {"count": -1}}
        ]
        
        cursor = col.aggregate(pipeline)
        results = await cursor.to_list(length=50)
        
        labels = [r["crime_type"] for r in results if r["crime_type"]]
        values = [r["count"] for r in results if r["crime_type"]]
        
        return {
            "type": "pie",
            "labels": labels,
            "values": values
        }

    async def get_yearly_distribution(self, district: str = None) -> Dict[str, Any]:
        """
        Yearly distribution of crime records.
        """
        col = get_collection("crime_records")
        match_stage = {}
        if district:
            match_stage["district"] = {"$regex": f"^{district}$", "$options": "i"}

        pipeline = [
            {"$match": match_stage} if match_stage else {"$match": {}},
            {
                "$group": {
                    "_id": {"$year": "$date"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "year": {"$toString": "$_id"},
                    "count": 1
                }
            },
            {"$sort": {"year": 1}}
        ]
        
        cursor = col.aggregate(pipeline)
        results = await cursor.to_list(length=10)
        
        labels = [r["year"] for r in results]
        values = [r["count"] for r in results]
        
        return {
            "type": "bar",
            "labels": labels,
            "values": values
        }
