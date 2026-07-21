from typing import List, Optional, Dict, Any
from app.repositories.crime_repository import CrimeRepository
from app.models.crime import CrimeRecord
from app.schemas.crime_schema import CrimeCreate
from app.utils.helpers import generate_uuid

class CrimeService:
    def __init__(self):
        self.repo = CrimeRepository()

    async def create_crime(self, crime_in: CrimeCreate) -> Dict[str, Any]:
        # Formulate full CrimeRecord from input
        location = {
            "type": "Point",
            "coordinates": [crime_in.longitude, crime_in.latitude]
        }
        
        crime_rec = CrimeRecord(
            crime_id=crime_in.crime_id or generate_uuid("CR-"),
            FIR_number=crime_in.FIR_number,
            crime_type=crime_in.crime_type,
            crime_category=crime_in.crime_category,
            crime_subcategory=crime_in.crime_subcategory,
            date=crime_in.date,
            time=crime_in.time,
            district=crime_in.district,
            police_station=crime_in.police_station,
            latitude=crime_in.latitude,
            longitude=crime_in.longitude,
            victim=crime_in.victim,
            suspect=crime_in.suspect,
            status=crime_in.status,
            sections=crime_in.sections,
            description=crime_in.description,
            weapon=crime_in.weapon,
            vehicle=crime_in.vehicle,
            location=location
        )
        return await self.repo.create(crime_rec)

    async def get_crime_by_id(self, crime_id: str) -> Optional[Dict[str, Any]]:
        return await self.repo.get_by_id(crime_id)

    async def search_crimes(self, filters: Dict[str, Any], limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
        return await self.repo.search(filters, limit, skip)

    async def update_crime(self, crime_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.repo.update(crime_id, update_data)

    async def delete_crime(self, crime_id: str) -> bool:
        return await self.repo.delete(crime_id)
