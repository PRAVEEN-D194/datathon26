"""
SurakshaAI - Data Generator for Karnataka State Police (KSP) Crime Database
Generates realistic synthetic crime datasets, police station metadata, and criminal network graphs.
Author: Member 4 (Data Engineer & Visualization Specialist)
"""

import os
import json
import random
import pandas as pd
from datetime import datetime, timedelta

# Create data directory if it doesn't exist
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Karnataka Districts & Key Stations with lat/long centroids
DISTRICTS = {
    "Bengaluru City": {
        "stations": ["Koramangala PS", "Indiranagar PS", "Whitefield PS", "Cubbon Park PS", "Jayanagar PS", "Electronic City PS", "Hebbal PS", "Rajajinagar PS"],
        "lat": 12.9716, "lng": 77.5946, "radius": 0.15
    },
    "Mysuru": {
        "stations": ["Devaraja PS", "Nazarbad PS", "Vidyaranyapuram PS", "Kuuvempunagar PS", "Lashkar PS"],
        "lat": 12.2958, "lng": 76.6394, "radius": 0.08
    },
    "Hubballi-Dharwad": {
        "stations": ["Suburban PS Hubballi", "Bendigeri PS", "Dharwad Town PS", "Vidyanagar PS"],
        "lat": 15.3647, "lng": 75.1240, "radius": 0.09
    },
    "Mangaluru": {
        "stations": ["Barkhe PS", "Pandeshwar PS", "Kadri PS", "Urwa PS", "Ullal PS"],
        "lat": 12.9141, "lng": 74.8560, "radius": 0.07
    },
    "Belagavi": {
        "stations": ["Khade Bazar PS", "Camp PS", "Tilakwadi PS", "APMC PS"],
        "lat": 15.8497, "lng": 74.4977, "radius": 0.08
    },
    "Kalaburagi": {
        "stations": ["Brahampur PS", "M B Nagar PS", "Chowk PS", "Station Bazar PS"],
        "lat": 17.3297, "lng": 76.8343, "radius": 0.08
    },
    "Ballari": {
        "stations": ["Brucepet PS", "Gandhinagar PS", "Cowled Bazar PS"],
        "lat": 15.1394, "lng": 76.9214, "radius": 0.07
    },
    "Tumakuru": {
        "stations": ["Town PS Tumakuru", "New Extension PS", "Kyathsandra PS"],
        "lat": 13.3409, "lng": 77.1006, "radius": 0.06
    }
}

CRIME_CATEGORIES = {
    "Cybercrime": {
        "subs": ["Phishing / OTP Fraud", "Crypto Scam", "Identity Theft", "Sextortion", "Financial Fraud"],
        "severity": (4, 8),
        "mo": ["Posing as Bank Executive", "Fake Tech Support", "Malware Link via WhatsApp", "Phishing Site"]
    },
    "Chain Snatching & Theft": {
        "subs": ["Two-Wheeler Chain Snatching", "Mobile Theft", "House Burglary", "Vehicle Theft"],
        "severity": (3, 7),
        "mo": ["Pillion rider snatching on Pulsar bike", "Unlocked house entry at night", "Master key ignition"]
    },
    "Narcotics": {
        "subs": ["Ganja Possession", "MDMA / Synthetic Drugs", "Inter-State Drug Trafficking"],
        "severity": (6, 10),
        "mo": ["Courier shipment concealed in electronics", "Darkweb ordering + Dead drop", "Near college campuses"]
    },
    "Robbery & Extortion": {
        "subs": ["Armed Robbery", "Extortion Call", "Highway Dacoity"],
        "severity": (7, 10),
        "mo": ["Sharp weapon threat at night", "Posing as local gang member", "Blocking highway with lorry"]
    },
    "Assault & Violent Crime": {
        "subs": ["Street Brawl", "Group Assault", "Grievous Hurt"],
        "severity": (5, 9),
        "mo": ["Altercation near bar/liquor shop", "Group clash over property dispute", "Pre-meditated attack"]
    },
    "Commercial Fraud": {
        "subs": ["Real Estate Scam", "Ponzi Scheme", "Job Fraud"],
        "severity": (4, 8),
        "mo": ["Fake government sanction letter", "High return investment scheme", "Fake visa offer"]
    }
}

SUSPECT_POOL = [
    {"id": "SUS-1001", "name": "Ramesh 'Blade' Kumar", "alias": "Blade Ramesh", "gang": "MG Road Gang", "history": 7},
    {"id": "SUS-1002", "name": "Syed 'Crypto' Imran", "alias": "Hacker Imran", "gang": "DarkNet Syndicate", "history": 4},
    {"id": "SUS-1003", "name": "Manjunath V", "alias": "Bullet Manja", "gang": "Koramangala Network", "history": 9},
    {"id": "SUS-1004", "name": "Kiran @ Shadow", "alias": "Shadow Kiran", "gang": "MG Road Gang", "history": 5},
    {"id": "SUS-1005", "name": "Vikram Singh", "alias": "Vicky Fraud", "gang": "North India Cyber Syndicate", "history": 6},
    {"id": "SUS-1006", "name": "Anil 'Snake' Shetty", "alias": "Snake Anil", "gang": "Coastal Smugglers", "history": 8},
    {"id": "SUS-1007", "name": "Praveen Gowda", "alias": "Appu", "gang": "Koramangala Network", "history": 3},
    {"id": "SUS-1008", "name": "Deepak Sharma", "alias": "Doctor", "gang": "DarkNet Syndicate", "history": 5},
    {"id": "SUS-1009", "name": "Farooq Ahmed", "alias": "Bhaijan", "gang": "Coastal Smugglers", "history": 11},
    {"id": "SUS-1010", "name": "Suresh 'Fast' Reddy", "alias": "Fast Reddy", "gang": "MG Road Gang", "history": 6}
]

STATUSES = ["Under Investigation", "Solved", "Pending", "Charge Sheeted", "Suspect Identified"]

def generate_crime_dataset(num_records=5000):
    start_date = datetime.now() - timedelta(days=365)
    records = []

    for i in range(1, num_records + 1):
        district_name = random.choice(list(DISTRICTS.keys()))
        dist_info = DISTRICTS[district_name]
        station_name = random.choice(dist_info["stations"])
        
        category_name = random.choice(list(CRIME_CATEGORIES.keys()))
        cat_info = CRIME_CATEGORIES[category_name]
        sub_cat = random.choice(cat_info["subs"])
        mo = random.choice(cat_info["mo"])
        
        # Lat / Lng jitter around district center
        lat = round(dist_info["lat"] + random.uniform(-dist_info["radius"], dist_info["radius"]), 6)
        lng = round(dist_info["lng"] + random.uniform(-dist_info["radius"], dist_info["radius"]), 6)
        
        # Incident date over last year
        random_days = random.randint(0, 365)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        incident_dt = start_date + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
        
        severity = random.randint(cat_info["severity"][0], cat_info["severity"][1])
        status = random.choice(STATUSES)
        
        # Assign suspect for ~40% cases
        if random.random() < 0.45:
            suspect = random.choice(SUSPECT_POOL)
            suspect_id = suspect["id"]
            suspect_name = suspect["name"]
            gang_name = suspect["gang"]
        else:
            suspect_id = "UNKNOWN"
            suspect_name = "Unidentified Suspect"
            gang_name = "None"
            
        estimated_loss = round(random.choice([0, 5000, 15000, 50000, 120000, 450000, 1500000]) * (severity / 5), 2)
        
        fir_num = f"FIR-{incident_dt.year}-{district_name[:3].upper()}-{1000 + i}"

        records.append({
            "fir_number": fir_num,
            "incident_date": incident_dt.strftime("%Y-%m-%d"),
            "incident_time": incident_dt.strftime("%H:%M:%S"),
            "timestamp": incident_dt.isoformat(),
            "district": district_name,
            "police_station": station_name,
            "crime_category": category_name,
            "sub_category": sub_cat,
            "latitude": lat,
            "longitude": lng,
            "severity_score": severity,
            "status": status,
            "modus_operandi": mo,
            "suspect_id": suspect_id,
            "suspect_name": suspect_name,
            "gang_affiliation": gang_name,
            "estimated_loss_inr": estimated_loss,
            "is_cybercrime": 1 if category_name == "Cybercrime" else 0,
            "repeat_offender": 1 if suspect_id != "UNKNOWN" and random.random() > 0.3 else 0
        })

    df = pd.DataFrame(records)
    csv_path = os.path.join(DATA_DIR, "ksp_crime_dataset.csv")
    df.to_csv(csv_path, index=False)
    print(f"[+] Successfully generated {num_records} crime records -> {csv_path}")
    return df

def generate_network_data():
    nodes = []
    links = []

    # Add Suspect Nodes
    for s in SUSPECT_POOL:
        nodes.append({
            "id": s["id"],
            "label": s["name"],
            "alias": s["alias"],
            "type": "suspect",
            "group": s["gang"],
            "prior_cases": s["history"],
            "risk_level": "HIGH" if s["history"] > 6 else "MEDIUM"
        })

    # Add Gang Nodes
    gangs = list(set(s["gang"] for s in SUSPECT_POOL))
    for g in gangs:
        nodes.append({
            "id": f"GANG-{g.replace(' ', '_').upper()}",
            "label": g,
            "type": "gang",
            "group": g,
            "risk_level": "CRITICAL"
        })
        
    # Add Connections (Suspect -> Gang & Suspect -> Co-Accused Suspect)
    for s in SUSPECT_POOL:
        # Link to Gang
        links.append({
            "source": s["id"],
            "target": f"GANG-{s['gang'].replace(' ', '_').upper()}",
            "relation": "MEMBER_OF",
            "weight": 5
        })

    # Add inter-suspect co-accused links
    predefined_links = [
        ("SUS-1001", "SUS-1004", "CO_ACCUSED_BURGLARY", 4),
        ("SUS-1001", "SUS-1010", "ARMED_ROBBERY_PARTNER", 5),
        ("SUS-1002", "SUS-1005", "CYBER_FINANCIAL_FRAUD", 4),
        ("SUS-1002", "SUS-1008", "DARKWEB_CRYPTO_NODE", 3),
        ("SUS-1003", "SUS-1007", "VEHICLE_THEFT_RING", 5),
        ("SUS-1006", "SUS-1009", "NARCOTICS_DISTRIBUTION", 6),
        ("SUS-1004", "SUS-1010", "CHAIN_SNATCHING_MO", 3)
    ]
    for src, tgt, rel, w in predefined_links:
        links.append({
            "source": src,
            "target": tgt,
            "relation": rel,
            "weight": w
        })

    network_data = {"nodes": nodes, "links": links}
    json_path = os.path.join(DATA_DIR, "ksp_offenders_network.json")
    with open(json_path, "w") as f:
        json.dump(network_data, f, indent=2)
    print(f"[+] Successfully generated criminal network graph -> {json_path}")
    return network_data

def generate_district_summary():
    dist_data = []
    for d, info in DISTRICTS.items():
        dist_data.append({
            "district": d,
            "station_count": len(info["stations"]),
            "stations": info["stations"],
            "latitude": info["lat"],
            "longitude": info["lng"]
        })
    path = os.path.join(DATA_DIR, "ksp_districts.json")
    with open(path, "w") as f:
        json.dump(dist_data, f, indent=2)
    print(f"[+] Successfully generated district station metadata -> {path}")

if __name__ == "__main__":
    generate_crime_dataset(5000)
    generate_network_data()
    generate_district_summary()
