from typing import List, Dict, Any
import networkx as G_NX

def build_network_elements(networks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build NetworkX graph from database records and extract nodes/edges.
    """
    g = G_NX.Graph()
    
    # Add nodes and edges
    for net in networks:
        criminal_id = net.get("criminal_id")
        name = net.get("name", criminal_id)
        crimes = net.get("associated_crimes", [])
        
        # Add primary criminal node
        g.add_node(
            criminal_id,
            label=name,
            group="Criminal",
            val=max(len(crimes), 1)
        )
        
        # Add relationships
        for conn in net.get("connections", []):
            target_id = conn.get("criminal_id")
            rel_type = conn.get("relation_type", "Associate")
            weight = conn.get("weight", 1.0)
            
            # Ensure target node exists
            if target_id not in g:
                g.add_node(target_id, label=target_id, group="Criminal", val=1)
                
            g.add_edge(criminal_id, target_id, label=rel_type, weight=weight)
            
    # Calculate degree centrality and page rank
    try:
        centrality = G_NX.degree_centrality(g)
        for nid in g.nodes:
            g.nodes[nid]["val"] = int(centrality[nid] * 10) + 1
    except Exception:
        pass

    # Build the schema-compliant node/edge output
    nodes = []
    for nid, attrs in g.nodes(data=True):
        nodes.append({
            "id": nid,
            "label": attrs.get("label", nid),
            "group": attrs.get("group", "Criminal"),
            "val": attrs.get("val", 1)
        })
        
    edges = []
    for u, v, attrs in g.edges(data=True):
        edges.append({
            "source": u,
            "target": v,
            "label": attrs.get("label", "Associate"),
            "weight": attrs.get("weight", 1.0)
        })
        
    return {
        "nodes": nodes,
        "edges": edges
    }

def find_gang_clusters(networks: List[Dict[str, Any]]) -> List[List[str]]:
    """
    Find community clusters in the criminal network.
    """
    g = G_NX.Graph()
    for net in networks:
        u = net.get("criminal_id")
        g.add_node(u)
        for conn in net.get("connections", []):
            v = conn.get("criminal_id")
            g.add_edge(u, v)
            
    try:
        # Using NetworkX community label propagation or modularity methods
        from networkx.algorithms import community
        clusters = community.label_propagation_communities(g)
        return [list(c) for c in clusters]
    except Exception:
        # Fallback to connected components if community algorithm fails or has empty graphs
        try:
            comps = G_NX.connected_components(g)
            return [list(c) for c in comps]
        except Exception:
            return []
