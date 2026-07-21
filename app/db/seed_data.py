import os
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import init_db, SessionLocal, CrimeIncident, Offender, incident_offender_association, engine

# Set random seed for reproducibility
random.seed(42)

DISTRICTS = {
    "Bengaluru": {
        "coords": (12.9716, 77.5946),
        "stations": ["Koramangala PS", "Indiranagar PS", "Whitefield PS", "Cubbon Park PS", "Cyber Crime PS North", "Jayanagar PS"]
    },
    "Mysuru": {
        "coords": (12.2958, 76.6394),
        "stations": ["Devaraja PS", "Lashkar PS", "Vidyaranyapuram PS", "Vijayanagar PS", "Mysuru Cyber PS"]
    },
    "Hubballi-Dharwada": {
        "coords": (15.3647, 75.1240),
        "stations": ["Suburban PS Hubballi", "Dharwada Town PS", "Vidyagiri PS", "Bendigeri PS"]
    },
    "Mangaluru": {
        "coords": (12.9141, 74.8560),
        "stations": ["Pandeshwar PS", "Kadri PS", "Urwa PS", "Mangaluru Cyber Crime PS"]
    },
    "Belagavi": {
        "coords": (15.8497, 74.4977),
        "stations": ["Khade Bazar PS", "Camp PS Belagavi", "Udyambag PS", "Market PS"]
    }
}

CRIME_TYPES = {
    "Cyber Crime": {
        "ipc": "IPC 420 (Cheating), IT Act Sec 66D (Cheating by personation using computer resource)",
        "summaries": [
            "Complainant reported loss of Rs. 1.5 Lakhs in credit card phishing scam.",
            "Victim clicked on a malicious link promising Work From Home jobs and lost money.",
            "Unauthorized access and ransomware attack on local commercial system.",
            "Online identity theft where perpetrator created fake profile to extort funds.",
            "Crypto investment scam reported via WhatsApp group link."
        ]
    },
    "Theft": {
        "ipc": "IPC 379 (Theft), IPC 34 (Acts done by several persons in furtherance of common intention)",
        "summaries": [
            "Two-wheeler vehicle parked outside house stolen at night.",
            "Gold chain and cash stolen from a residential house when owners were away.",
            "Mobile phone snatched from pedestrian while walking near public park.",
            "Laptop and electronics stolen from office premises during weekend.",
            "House break-in reported during daytime, ornaments stolen."
        ]
    },
    "Narcotics": {
        "ipc": "NDPS Act Sec 20 (Punishment for contravention in relation to cannabis plant and cannabis)",
        "summaries": [
            "Police raid conducted, seized 2.5 kg of Ganja from a peddler near college campus.",
            "Illegal possession and sale of MDMA synthetic drugs near tech park area.",
            "Accused caught with banned narcotics substances during vehicle checkpoint checking.",
            "Seizure of contraband drugs from courier parcel center.",
            "Raid on warehouse resulting in arrest of drug distributor and stash seizure."
        ]
    },
    "Crimes Against Women": {
        "ipc": "IPC 354 (Assault or criminal force to woman with intent to outrage modesty), IPC 498A (Husband or relative of husband of a woman subjecting her to cruelty)",
        "summaries": [
            "Victim reported harassment and outraging of modesty by a known offender at workplace.",
            "Complaint of domestic violence and mental harassment filed against husband.",
            "Eve-teasing incident reported near bus stop during evening hours.",
            "Stalking complaint filed by student against a repeat offender.",
            "Assault on woman during domestic dispute between neighbors."
        ]
    },
    "Assault": {
        "ipc": "IPC 324 (Voluntarily causing hurt by dangerous weapons), IPC 506 (Criminal intimidation)",
        "summaries": [
            "Altercation between two groups over parking dispute led to physical assault.",
            "Accused assaulted complainant with a wooden stick during road rage incident.",
            "Physical fight reported near local bar, one victim injured.",
            "Group clash due to personal animosity, leading to injuries and criminal intimidation.",
            "Assault on shopkeeper by a customer over billing dispute."
        ]
    }
}

OFFENDERS_POOL = [
    {"name": "Ramesh Kumar", "age": 28, "gender": "Male", "crime": "Theft"},
    {"name": "Anil K.S.", "age": 32, "gender": "Male", "crime": "Cyber Crime"},
    {"name": "Sunitha Rao", "age": 25, "gender": "Female", "crime": "Cyber Crime"},
    {"name": "Syed Imran", "age": 30, "gender": "Male", "crime": "Narcotics"},
    {"name": "Pradeep Hegde", "age": 41, "gender": "Male", "crime": "Assault"},
    {"name": "Kiran Naik", "age": 22, "gender": "Male", "crime": "Theft"},
    {"name": "Manjunath S.", "age": 35, "gender": "Male", "crime": "Theft"},
    {"name": "Vikas Gowda", "age": 29, "gender": "Male", "crime": "Narcotics"},
    {"name": "Vijay Shetty", "age": 38, "gender": "Male", "crime": "Assault"},
    {"name": "Farhan Khan", "age": 27, "gender": "Male", "crime": "Narcotics"},
    {"name": "Deepak Lal", "age": 34, "gender": "Male", "crime": "Cyber Crime"},
    {"name": "Harish Poojary", "age": 26, "gender": "Male", "crime": "Theft"}
]

def seed_database():
    init_db()
    db = SessionLocal()
    
    try:
        # Check if already seeded
        if db.query(CrimeIncident).count() > 0:
            print("Database already contains data. Seeding skipped.")
            return

        print("Seeding offenders...")
        offender_objects = []
        for i, off in enumerate(OFFENDERS_POOL):
            off_id = f"OFF-{1000 + i}"
            o = Offender(
                offender_id=off_id,
                name=off["name"],
                age=off["age"],
                gender=off["gender"],
                primary_crime_type=off["crime"]
            )
            db.add(o)
            offender_objects.append(o)
        db.commit()

        print("Seeding crime incidents...")
        # Create incidents spread over the last 500 days
        start_date = datetime.now() - timedelta(days=500)
        
        incidents = []
        for i in range(1, 1201):  # Generate 1200 crime records
            district = random.choice(list(DISTRICTS.keys()))
            dist_info = DISTRICTS[district]
            station = random.choice(dist_info["stations"])
            crime_head = random.choice(list(CRIME_TYPES.keys()))
            crime_info = CRIME_TYPES[crime_head]
            
            # Generate random coordinate within radius of district center
            lat_center, lon_center = dist_info["coords"]
            lat = lat_center + random.uniform(-0.04, 0.04)
            lon = lon_center + random.uniform(-0.04, 0.04)
            
            # Timestamp with some seasonality / trend
            # e.g., higher probability of cyber crimes recently
            days_offset = random.randint(0, 500)
            date_occ = start_date + timedelta(days=days_offset, hours=random.randint(0, 23), minutes=random.randint(0, 59))
            date_rep = date_occ + timedelta(hours=random.randint(1, 48))
            
            inc_id = f"KSP-{date_occ.strftime('%Y')}-{10000 + i}"
            status = random.choices(["Under Investigation", "Solved", "Chargesheeted"], weights=[0.4, 0.4, 0.2])[0]
            summary = random.choice(crime_info["summaries"])
            
            incident = CrimeIncident(
                incident_id=inc_id,
                district=district,
                station_name=station,
                crime_head=crime_head,
                ipc_sections=crime_info["ipc"],
                date_reported=date_rep,
                date_occurrence=date_occ,
                latitude=lat,
                longitude=lon,
                status=status,
                summary=summary
            )
            
            # Offender linkage (Gangs and Repeat Offenders)
            # 15% chance of attaching known offenders
            if random.random() < 0.15:
                # Select 1 or 2 random offenders from the pool
                num_offs = random.choice([1, 2])
                associated_offs = random.sample(offender_objects, num_offs)
                for o in associated_offs:
                    # Link via association table
                    # To do this with SQLAlchemy core table or relation:
                    # We can use the connection or model relationship if defined, 
                    # but here we can insert directly into association table
                    # let's run insert statements or bind them. Let's do it using SQL connection execution
                    pass
                
                # Keep track of links to insert at the end
                incident._seeded_offenders = [o.offender_id for o in associated_offs]
            else:
                incident._seeded_offenders = []

            db.add(incident)
            incidents.append(incident)
            
        db.commit()

        # Insert relations into association table
        print("Linking co-offenders and repeat offenders...")
        conn = engine.connect()
        for inc in incidents:
            for off_id in inc._seeded_offenders:
                conn.execute(
                    incident_offender_association.insert().values(
                        incident_id=inc.incident_id,
                        offender_id=off_id
                    )
                )
        conn.commit()
        conn.close()

        print(f"Successfully seeded database with {len(incidents)} crime records and {len(offender_objects)} offenders.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
