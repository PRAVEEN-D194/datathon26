import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///D:/Datathon - Cyber Nexus/crime_records.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Association table for incident and offender relationships (co-offending network)
incident_offender_association = Table(
    "incident_offender",
    Base.metadata,
    Column("incident_id", String, ForeignKey("crime_incidents.incident_id")),
    Column("offender_id", String, ForeignKey("offenders.offender_id"))
)

class CrimeIncident(Base):
    __tablename__ = "crime_incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, unique=True, index=True, nullable=False)
    district = Column(String, index=True, nullable=False)
    station_name = Column(String, index=True, nullable=False)
    crime_head = Column(String, index=True, nullable=False)  # e.g., Cyber Crime, Theft, Murder, etc.
    ipc_sections = Column(String, nullable=False)  # e.g., "IPC 379, IPC 34"
    date_reported = Column(DateTime, nullable=False)
    date_occurrence = Column(DateTime, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    status = Column(String, default="Under Investigation")  # Investigating, Solved, Chargesheeted, Closed
    summary = Column(String, nullable=True)

class Offender(Base):
    __tablename__ = "offenders"

    id = Column(Integer, primary_key=True, index=True)
    offender_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    primary_crime_type = Column(String, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
