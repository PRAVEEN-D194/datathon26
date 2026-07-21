from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.core.database import get_collection
from app.models.crime import CrimeRecord

class CrimeRepository:
    @staticmethod
    def _to_dict(crime: CrimeRecord) -> Dict[str, Any]:
        data = crime.model_dump(by_alias=True, exclude_none=True)
        if "_id" in data and isinstance(data["_id"], str):
            data["_id"] = ObjectId(data["_id"])
        
        # Ensure location GeoJSON is properly formatted
        if "location" not in data and "latitude" in data and "longitude" in data:
            data["location"] = {
                "type": "Point",
                "coordinates": [data["longitude"], data["latitude"]]
            }
        return data

    @staticmethod
    def _to_model(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if doc is None:
            return None
        doc["_id"] = str(doc["_id"])
        return doc

    async def get_by_id(self, crime_record_id: str) -> Optional[Dict[str, Any]]:
        col = get_collection("crime_records")
        # Try finding by Mongo ObjectId, then by user-facing crime_id
        doc = None
        if ObjectId.is_valid(crime_record_id):
            doc = await col.find_one({"_id": ObjectId(crime_record_id)})
        if not doc:
            doc = await col.find_one({"crime_id": crime_record_id})
        return self._to_model(doc)

    async def create(self, crime: CrimeRecord) -> Dict[str, Any]:
        col = get_collection("crime_records")
        data = self._to_dict(crime)
        res = await col.insert_one(data)
        doc = await col.find_one({"_id": res.inserted_id})
        return self._to_model(doc)

    async def search(self, filters: Dict[str, Any], limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
        col = get_collection("crime_records")
        query = {}
        
        if filters.get("district"):
            # Case insensitive regex match for flexibility
            query["district"] = {"$regex": f"^{filters['district']}$", "$options": "i"}
        if filters.get("crime_type"):
            query["crime_type"] = {"$regex": f"^{filters['crime_type']}$", "$options": "i"}
        if filters.get("police_station"):
            query["police_station"] = {"$regex": f"^{filters['police_station']}$", "$options": "i"}
        if filters.get("status"):
            query["status"] = filters["status"]
            
        # Date queries (range filter)
        if filters.get("start_date") or filters.get("end_date"):
            query["date"] = {}
            if filters.get("start_date"):
                query["date"]["$gte"] = filters["start_date"]
            if filters.get("end_date"):
                query["date"]["$lte"] = filters["end_date"]

        # Geospatial query if coordinate + max distance (meters) is provided
        if filters.get("latitude") and filters.get("longitude") and filters.get("radius_km"):
            radius_meters = float(filters["radius_km"]) * 1000
            query["location"] = {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [float(filters["longitude"]), float(filters["latitude"])]
                    },
                    "$maxDistance": radius_meters
                }
            }

        cursor = col.find(query).skip(skip).limit(limit).sort("date", -1)
        crimes = []
        async for doc in cursor:
            crimes.append(self._to_model(doc))
        return crimes

    async def update(self, crime_record_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        col = get_collection("crime_records")
        query = {}
        if ObjectId.is_valid(crime_record_id):
            query["_id"] = ObjectId(crime_record_id)
        else:
            query["crime_id"] = crime_record_id
            
        # Handle updating location when lat/long are updated
        if "latitude" in update_data or "longitude" in update_data:
            existing = await col.find_one(query)
            if existing:
                lat = update_data.get("latitude", existing.get("latitude"))
                lon = update_data.get("longitude", existing.get("longitude"))
                update_data["location"] = {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
                
        res = await col.update_one(query, {"$set": update_data})
        if res.modified_count > 0 or res.matched_count > 0:
            doc = await col.find_one(query)
            return self._to_model(doc)
        return None

    async def delete(self, crime_record_id: str) -> bool:
        col = get_collection("crime_records")
        query = {}
        if ObjectId.is_valid(crime_record_id):
            query["_id"] = ObjectId(crime_record_id)
        else:
            query["crime_id"] = crime_record_id
            
        res = await col.delete_one(query)
        return res.deleted_count > 0
