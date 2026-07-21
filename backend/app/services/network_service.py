from typing import List, Dict, Any, Optional
from app.core.database import get_collection
from app.utils.graph_utils import build_network_elements, find_gang_clusters
from app.ml.link_prediction import predict_criminal_links
from app.schemas.chat_schema import NetworkGraphData, GraphNode, GraphEdge

class NetworkService:
    async def get_criminal_network(self, criminal_id: str) -> NetworkGraphData:
        """
        Gets network connections for a specific criminal or the entire network if none specified.
        """
        col = get_collection("crime_network")
        
        # If criminal is specified, retrieve their network and their direct connections networks
        if criminal_id:
            root = await col.find_one({"criminal_id": criminal_id})
            if not root:
                # Return empty graph structure
                return NetworkGraphData(nodes=[], edges=[])
                
            # Collect criminal_ids of direct connections to build complete local graph
            connected_ids = [c.get("criminal_id") for c in root.get("connections", [])]
            ids_to_fetch = [criminal_id] + connected_ids
            
            cursor = col.find({"criminal_id": {"$in": ids_to_fetch}})
            networks = await cursor.to_list(length=100)
        else:
            # Get the whole network up to limit
            cursor = col.find()
            networks = await cursor.to_list(length=500)

        graph_elements = build_network_elements(networks)
        return NetworkGraphData(
            nodes=[GraphNode(**n) for n in graph_elements["nodes"]],
            edges=[GraphEdge(**e) for e in graph_elements["edges"]]
        )

    async def get_gang_clusters(self) -> List[Dict[str, Any]]:
        """
        Calculates clusters of criminals using network community algorithms.
        """
        col = get_collection("crime_network")
        cursor = col.find()
        networks = await cursor.to_list(length=1000)
        
        clusters = find_gang_clusters(networks)
        
        # Retrieve names for criminal IDs in clusters
        names_map = {n.get("criminal_id"): n.get("name", n.get("criminal_id")) for n in networks}
        
        formatted_clusters = []
        for idx, cluster in enumerate(clusters):
            members = []
            for cid in cluster:
                members.append({
                    "criminal_id": cid,
                    "name": names_map.get(cid, cid)
                })
            formatted_clusters.append({
                "cluster_id": f"GANG-CLUSTER-{idx+1:02d}",
                "members": members,
                "size": len(members)
            })
            
        # Sort by cluster size descending
        return sorted(formatted_clusters, key=lambda x: x["size"], reverse=True)

    async def get_repeat_offenders(self, min_crimes: int = 2, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Identify repeat suspects using aggregation pipelines on crime records.
        """
        col = get_collection("crime_records")
        pipeline = [
            # Only aggregate if suspect has criminal_id or name
            {"$match": {"suspect.criminal_id": {"$ne": None}}},
            {
                "$group": {
                    "_id": "$suspect.criminal_id",
                    "name": {"$first": "$suspect.name"},
                    "crime_count": {"$sum": 1},
                    "crimes": {"$push": {
                        "crime_id": "$crime_id",
                        "FIR_number": "$FIR_number",
                        "crime_type": "$crime_type",
                        "date": "$date",
                        "status": "$status"
                    }},
                    "districts": {"$addToSet": "$district"}
                }
            },
            {"$match": {"crime_count": {"$gte": min_crimes}}},
            {"$sort": {"crime_count": -1}},
            {"$limit": limit},
            {
                "$project": {
                    "_id": 0,
                    "criminal_id": "$_id",
                    "name": 1,
                    "crime_count": 1,
                    "crimes": 1,
                    "districts": 1
                }
            }
        ]
        
        cursor = col.aggregate(pipeline)
        return await cursor.to_list(length=limit)

    async def get_predicted_links(self) -> List[Dict[str, Any]]:
        """
        Recommends potential accomplice link predictions.
        """
        col = get_collection("crime_network")
        cursor = col.find()
        networks = await cursor.to_list(length=1000)
        return predict_criminal_links(networks)
