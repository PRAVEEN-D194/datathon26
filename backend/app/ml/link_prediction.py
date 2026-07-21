import networkx as G_NX
from typing import List, Dict, Any

def predict_criminal_links(networks: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Predict hidden/future links between criminals in the network 
    using NetworkX Jaccard Coefficient algorithm.
    """
    g = G_NX.Graph()
    criminal_names = {}
    
    # 1. Build the network graph
    for net in networks:
        u = net.get("criminal_id")
        name = net.get("name", u)
        criminal_names[u] = name
        g.add_node(u)
        
        for conn in net.get("connections", []):
            v = conn.get("criminal_id")
            if u != v:
                g.add_edge(u, v)

    # If graph has too few edges or is empty, we cannot predict
    if g.number_of_edges() < 1:
        return []

    # 2. Compute Jaccard Coefficients for all unconnected pairs
    predicted_links = []
    try:
        preds = G_NX.jaccard_coefficient(g)
        for u, v, score in preds:
            if score > 0.0:  # Only report if they share at least one mutual neighbor
                predicted_links.append({
                    "criminal_a_id": u,
                    "criminal_a_name": criminal_names.get(u, u),
                    "criminal_b_id": v,
                    "criminal_b_name": criminal_names.get(v, v),
                    "score": round(float(score), 2),
                    "reason": f"Shares mutual accomplice(s)"
                })
    except Exception:
        pass

    # Sort by score descending
    predicted_links = sorted(predicted_links, key=lambda x: x["score"], reverse=True)
    return predicted_links[:top_n]
