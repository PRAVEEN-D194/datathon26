"""
SurakshaAI - Network & Link Analytics Engine
Performs criminal relationship mapping, gang detection, and repeat offender link analysis.
Author: Member 4 (Data Engineer & Visualization Specialist)
"""

import os
import json

NETWORK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ksp_offenders_network.json")

class NetworkAnalyticsEngine:
    def __init__(self, json_path=NETWORK_DATA_PATH):
        self.json_path = json_path
        self._load_network()

    def _load_network(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as f:
                self.network_data = json.load(f)
        else:
            self.network_data = {"nodes": [], "links": []}

    def get_full_graph(self):
        """Returns the entire suspect-gang network graph."""
        return self.network_data

    def get_suspect_network(self, suspect_query):
        """Filter graph centered on a specific suspect or gang."""
        nodes = self.network_data.get("nodes", [])
        links = self.network_data.get("links", [])

        target_ids = set()

        # Find target node by ID, label, or alias
        for node in nodes:
            name = node.get("label", "").lower()
            alias = node.get("alias", "").lower()
            nid = node.get("id", "").lower()
            q = suspect_query.lower()
            if q in name or q in alias or q in nid:
                target_ids.add(node["id"])

        if not target_ids:
            # Return top 15 nodes default if not found specifically
            return {
                "nodes": nodes[:15],
                "links": links[:20],
                "target_found": False,
                "query": suspect_query
            }

        # 1-hop connected nodes
        connected_ids = set(target_ids)
        filtered_links = []

        for link in links:
            src = link["source"]
            tgt = link["target"]
            if src in target_ids or tgt in target_ids:
                connected_ids.add(src)
                connected_ids.add(tgt)
                filtered_links.append(link)

        filtered_nodes = [n for n in nodes if n["id"] in connected_ids]

        return {
            "nodes": filtered_nodes,
            "links": filtered_links,
            "target_found": True,
            "query": suspect_query,
            "central_suspects": list(target_ids)
        }

    def get_repeat_offenders_summary(self):
        """Returns key statistics on high-risk repeat offender suspects."""
        nodes = self.network_data.get("nodes", [])
        suspects = [n for n in nodes if n.get("type") == "suspect"]
        
        sorted_suspects = sorted(suspects, key=lambda x: x.get("prior_cases", 0), reverse=True)
        
        return {
            "total_tracked_suspects": len(suspects),
            "high_risk_suspects": [s for s in sorted_suspects if s.get("risk_level") == "HIGH"],
            "top_repeat_offenders": sorted_suspects[:5]
        }

network_engine = NetworkAnalyticsEngine()
