import asyncio
import os
import sys
from datetime import datetime, timedelta
import random

# Adjust path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Database, get_collection
from app.core.security import get_password_hash
from app.core.logging import logger

# Config parameters
DISTRICTS = [
    {
        "name": "Bengaluru City",
        "code": "KA-BC",
        "headquarters": "Bengaluru",
        "population": 8443675,
        "area_sq_km": 709.0,
        "police_stations_count": 108,
        "coordinates": [12.9716, 77.5946]
    },
    {
        "name": "Mysuru",
        "code": "KA-MY",
        "headquarters": "Mysuru",
        "population": 1022442,
        "area_sq_km": 152.0,
        "police_stations_count": 28,
        "coordinates": [12.2958, 76.6394]
    },
    {
        "name": "Mangaluru",
        "code": "KA-MN",
        "headquarters": "Mangaluru",
        "population": 623841,
        "area_sq_km": 132.0,
        "police_stations_count": 18,
        "coordinates": [12.9141, 74.8560]
    },
    {
        "name": "Hubballi-Dharwad",
        "code": "KA-HD",
        "headquarters": "Dharwad",
        "population": 943857,
        "area_sq_km": 213.0,
        "police_stations_count": 24,
        "coordinates": [15.3647, 75.1240]
    },
    {
        "name": "Udupi",
        "code": "KA-UD",
        "headquarters": "Udupi",
        "population": 268689,
        "area_sq_km": 68.0,
        "police_stations_count": 12,
        "coordinates": [13.3409, 74.7421]
    }
]

CRIME_TYPES = [
    ("Theft", "Property Crime", "Motor Vehicle Theft", ["379 IPC", "303 BNS"]),
    ("Assault", "Violent Crime", "Grievous Hurt", ["323 IPC", "324 IPC", "115 BNS"]),
    ("Cyber Crime", "Economic Offence", "Phishing Fraud", ["66D IT Act", "420 IPC", "318 BNS"]),
    ("Murder", "Violent Crime", "Homicide", ["302 IPC", "103 BNS"]),
    ("Kidnapping", "Violent Crime", "Kidnapping for Ransom", ["364A IPC", "140 BNS"]),
    ("Drug Trafficking", "NDPS Act Case", "Commercial Quantity Sale", ["20 NDPS Act", "22 NDPS Act"])
]

SUSPECTS = [
    {"criminal_id": "CRIM-001", "name": "Kiran 'Blade' Kumar", "age": 28, "gender": "Male"},
    {"criminal_id": "CRIM-002", "name": "Ramesh Kumar", "age": 32, "gender": "Male"},
    {"criminal_id": "CRIM-003", "name": "Shiva 'Soda' Raj", "age": 26, "gender": "Male"},
    {"criminal_id": "CRIM-004", "name": "Vijay 'Bullet' Shetty", "age": 35, "gender": "Male"},
    {"criminal_id": "CRIM-005", "name": "Anil 'Techie' Sen", "age": 24, "gender": "Male"},
    {"criminal_id": "CRIM-006", "name": "Unknown Suspect", "age": None, "gender": "Unknown"}
]

VICTIMS = [
    {"name": "Amit Sharma", "age": 34, "gender": "Male"},
    {"name": "Priyanka Gowda", "age": 29, "gender": "Female"},
    {"name": "Ravi Shastri", "age": 52, "gender": "Male"},
    {"name": "Deepa Rao", "age": 22, "gender": "Female"},
    {"name": "Karan Johar", "age": 41, "gender": "Male"}
]

WEAPONS = ["Knife", "Iron Rod", "Firearm", "None"]
VEHICLES = ["KA-01-HE-1234", "KA-09-MA-5678", "KA-20-UD-9999", "None"]
STATUSES = ["Under Investigation", "Charge-sheeted", "Closed"]

DESCRIPTIONS = {
    "Theft": "Theft of a parked two-wheeler from the shopping center parking lot.",
    "Assault": "Physical altercation outside a food court following a verbal dispute.",
    "Cyber Crime": "Victim was duped of money via a fraudulent bank verification link sent over SMS.",
    "Murder": "Victim found dead in an alleyway. Primary suspect fled the scene.",
    "Kidnapping": "Minor kidnapped from near school gate. Call for ransom received by parents.",
    "Drug Trafficking": "Suspect caught in possession of synthetic drugs intended for commercial distribution."
}

async def seed_database():
    logger.info("Initializing database connections for seeding...")
    await Database.connect_db()
    db = Database.db

    # 1. Clear existing collections
    collections_to_clear = [
        "users", "crime_records", "districts", 
        "chat_history", "crime_predictions", "crime_network", "alerts"
    ]
    for col_name in collections_to_clear:
        logger.info(f"Clearing collection: {col_name}")
        await db[col_name].delete_many({})

    # 2. Insert Users
    logger.info("Creating default users...")
    users = [
        {
            "name": "Super Admin",
            "email": "admin@ksp.gov.in",
            "password": get_password_hash("admin123"),
            "role": "admin",
            "createdAt": datetime.utcnow()
        },
        {
            "name": "Inspector Rajesh",
            "email": "officer@ksp.gov.in",
            "password": get_password_hash("officer123"),
            "role": "officer",
            "district": "Bengaluru City",
            "station": "Koramangala PS",
            "createdAt": datetime.utcnow()
        },
        {
            "name": "Analyst Suma",
            "email": "analyst@ksp.gov.in",
            "password": get_password_hash("analyst123"),
            "role": "analyst",
            "createdAt": datetime.utcnow()
        }
    ]
    await db.users.insert_many(users)
    logger.info(f"Seeded {len(users)} user profiles.")

    # 3. Insert District Configurations
    logger.info("Seeding districts...")
    await db.districts.insert_many(DISTRICTS)
    logger.info(f"Seeded {len(DISTRICTS)} district boundaries.")

    # 4. Insert Crime Records (generate 100 crimes spread over the last 12 months)
    logger.info("Generating realistic historical crime logs...")
    crimes = []
    base_date = datetime.utcnow() - timedelta(days=365)
    
    # Track crimes per criminal for the network links
    criminal_crime_map = {s["criminal_id"]: [] for s in SUSPECTS if s["criminal_id"] != "CRIM-006"}

    for i in range(1, 120):
        # Pick random parameters
        dist_meta = random.choice(DISTRICTS)
        crime_type, category, subcat, sections = random.choice(CRIME_TYPES)
        suspect = random.choice(SUSPECTS).copy()
        victim = random.choice(VICTIMS)
        
        # Calculate random date in past year
        crime_date = base_date + timedelta(
            days=random.randint(0, 360),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        # Jitter coordinates around the district center
        lat_jitter = random.uniform(-0.04, 0.04)
        lon_jitter = random.uniform(-0.04, 0.04)
        lat = dist_meta["coordinates"][0] + lat_jitter
        lon = dist_meta["coordinates"][1] + lon_jitter
        
        crime_id = f"CR-2026-{i:04d}"
        fir_number = f"FIR/{crime_date.year}/{i:03d}"
        
        # Map crimes back to criminal ids
        if suspect.get("criminal_id") and suspect["criminal_id"] != "CRIM-006":
            criminal_crime_map[suspect["criminal_id"]].append(crime_id)

        crimes.append({
            "crime_id": crime_id,
            "FIR_number": fir_number,
            "crime_type": crime_type,
            "crime_category": category,
            "crime_subcategory": subcat,
            "date": crime_date,
            "time": f"{crime_date.hour:02d}:{crime_date.minute:02d}",
            "district": dist_meta["name"],
            "police_station": f"{dist_meta['name'].split()[0]} Town PS",
            "latitude": lat,
            "longitude": lon,
            "victim": victim,
            "suspect": suspect,
            "status": random.choice(STATUSES),
            "sections": sections,
            "description": f"{DESCRIPTIONS[crime_type]} Incident observed in vicinity.",
            "weapon": random.choice(WEAPONS),
            "vehicle": random.choice(VEHICLES),
            "location": {
                "type": "Point",
                "coordinates": [lon, lat]
            }
        })
        
    await db.crime_records.insert_many(crimes)
    logger.info(f"Seeded {len(crimes)} crime records.")

    # 5. Insert Crime Networks
    logger.info("Setting up criminal networks...")
    networks = [
        {
            "criminal_id": "CRIM-001",
            "name": "Kiran 'Blade' Kumar",
            "connections": [
                {"criminal_id": "CRIM-002", "relation_type": "Accomplice", "weight": 0.8},
                {"criminal_id": "CRIM-003", "relation_type": "Gang Member", "weight": 0.6}
            ],
            "associated_crimes": criminal_crime_map["CRIM-001"]
        },
        {
            "criminal_id": "CRIM-002",
            "name": "Ramesh Kumar",
            "connections": [
                {"criminal_id": "CRIM-001", "relation_type": "Accomplice", "weight": 0.8},
                {"criminal_id": "CRIM-004", "relation_type": "Logistics Helper", "weight": 0.5}
            ],
            "associated_crimes": criminal_crime_map["CRIM-002"]
        },
        {
            "criminal_id": "CRIM-003",
            "name": "Shiva 'Soda' Raj",
            "connections": [
                {"criminal_id": "CRIM-001", "relation_type": "Gang Member", "weight": 0.6},
                {"criminal_id": "CRIM-004", "relation_type": "Accomplice", "weight": 0.7}
            ],
            "associated_crimes": criminal_crime_map["CRIM-003"]
        },
        {
            "criminal_id": "CRIM-004",
            "name": "Vijay 'Bullet' Shetty",
            "connections": [
                {"criminal_id": "CRIM-002", "relation_type": "Logistics Helper", "weight": 0.5},
                {"criminal_id": "CRIM-003", "relation_type": "Accomplice", "weight": 0.7}
            ],
            "associated_crimes": criminal_crime_map["CRIM-004"]
        },
        {
            "criminal_id": "CRIM-005",
            "name": "Anil 'Techie' Sen",
            "connections": [],
            "associated_crimes": criminal_crime_map["CRIM-005"]
        }
    ]
    await db.crime_network.insert_many(networks)
    logger.info(f"Seeded {len(networks)} criminal network maps.")

    # 6. Insert Alerts
    logger.info("Creating initial warnings/alerts...")
    alerts = [
        {
            "district": "Bengaluru City",
            "message": "Critical spike in Cyber Phishing crimes detected. Broad warnings advised.",
            "severity": "Critical",
            "createdAt": datetime.utcnow()
        },
        {
            "district": "Mysuru",
            "message": "Seasonal robbery warning active for heritage tourist zones.",
            "severity": "Warning",
            "createdAt": datetime.utcnow() - timedelta(hours=12)
        },
        {
            "district": "Mangaluru",
            "message": "Routine surveillance alert active near port area boundaries.",
            "severity": "Info",
            "createdAt": datetime.utcnow() - timedelta(days=2)
        }
    ]
    await db.alerts.insert_many(alerts)
    logger.info(f"Seeded {len(alerts)} alerts.")

    logger.info("Database seeding successfully finished!")
    await Database.close_db()

if __name__ == "__main__":
    asyncio.run(seed_database())
