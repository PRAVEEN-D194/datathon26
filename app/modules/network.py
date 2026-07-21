import sqlite3
import pandas as pd
import networkx as nx

DB_PATH = "D:/Datathon - Cyber Nexus/crime_records.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def analyze_criminal_network():
    """
    Builds a co-offender network graph using NetworkX.
    Nodes: Offenders
    Edges: Co-offended in at least one crime incident
    """
    conn = get_db_connection()
    
    # Query all linkages between incidents and offenders
    query = """
        SELECT io.incident_id, io.offender_id, o.name, o.age, o.gender, o.primary_crime_type 
        FROM incident_offender io
        JOIN offenders o ON io.offender_id = o.offender_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    G = nx.Graph()
    
    # 1. Add all offender nodes with metadata
    offenders_dict = {}
    for _, row in df.iterrows():
        off_id = row['offender_id']
        if off_id not in offenders_dict:
            offenders_dict[off_id] = {
                "id": off_id,
                "name": row['name'],
                "age": int(row['age']),
                "gender": row['gender'],
                "primary_crime_type": row['primary_crime_type']
            }
            G.add_node(off_id, **offenders_dict[off_id])
            
    # 2. Add edges for co-offending relationships (offenders sharing same incident)
    incidents_groups = df.groupby('incident_id')['offender_id'].apply(list)
    for incident_id, offender_list in incidents_groups.items():
        if len(offender_list) > 1:
            # Create a fully connected clique for offenders in this incident
            for i in range(len(offender_list)):
                for j in range(i + 1, len(offender_list)):
                    u, v = offender_list[i], offender_list[j]
                    if G.has_edge(u, v):
                        G[u][v]['weight'] += 1
                    else:
                        G.add_edge(u, v, weight=1)
                        
    # 3. Graph metrics for intelligence insights
    degree_centrality = nx.degree_centrality(G) if len(G) > 0 else {}
    
    # Find clusters/gangs (connected components)
    components = list(nx.connected_components(G)) if len(G) > 0 else []
    gangs = []
    for idx, c in enumerate(components):
        if len(c) > 1:
            gangs.append({
                "gang_id": f"GANG-{idx+1}",
                "members": [offenders_dict[m]['name'] for m in c],
                "size": len(c)
            })
            
    # Build list of nodes with their centrality ranking
    nodes_out = []
    for n in G.nodes(data=True):
        node_id = n[0]
        node_data = n[1]
        node_data["centrality"] = round(degree_centrality.get(node_id, 0.0), 3)
        nodes_out.append(node_data)
        
    # Build list of edges/links
    links_out = []
    for u, v, data in G.edges(data=True):
        links_out.append({
            "source": u,
            "target": v,
            "weight": data.get("weight", 1)
        })
        
    explanation = f"Analyzed co-offending relations. Identified {len(gangs)} potential active criminal syndicates/gangs. Top offenders ranked by node centrality."
    
    return {
        "nodes": nodes_out,
        "links": links_out,
        "gangs": gangs,
        "explanation": explanation
    }

if __name__ == "__main__":
    print("Testing Criminal Network Analyzer...")
    network = analyze_criminal_network()
    print("Explanation:", network["explanation"])
    print("Detected Gangs:", network["gangs"])
    print("Total Nodes:", len(network["nodes"]))
    print("Total Links:", len(network["links"]))
