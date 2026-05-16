from typing import List, Optional
import sqlalchemy
from sqlalchemy import select, func
from src.models.db.job_profile import JobProfile
from src.repository.crud.base import BaseCRUDRepository

class JobProfileCRUDRepository(BaseCRUDRepository):
    async def get_summary(self) -> dict:
        """
        Returns a summary count of job profiles.
        Since status field doesn't exist yet, we return 0 for status-based counts.
        """
        query = select(func.count()).select_from(JobProfile)
        result = await self.async_session.execute(query)
        total_count = result.scalar() or 0
        
        return {
            "totalRoles": total_count,
            "pendingReview": 0,
            "approved": 0,
            "rejected": 0
        }

    async def list_profiles(self, category: Optional[str] = None) -> List[JobProfile]:
        query = select(JobProfile).order_by(JobProfile.created_at.desc())
        
        if category:
            # Filter by job_name as a fallback for category
            query = query.where(JobProfile.job_name.ilike(f"%{category}%"))
            
        result = await self.async_session.execute(query)
        return list(result.scalars().all())

    async def create_profile(self, title: str, description: Optional[str] = None) -> JobProfile:
        new_profile = JobProfile(job_name=title, job_description=description or "")
        self.async_session.add(new_profile)
        await self.async_session.flush()
        return new_profile

    async def delete_profile(self, profile_id: int) -> bool:
        query = select(JobProfile).where(JobProfile.id == profile_id)
        result = await self.async_session.execute(query)
        profile = result.scalar_one_or_none()
        if profile:
            await self.async_session.delete(profile)
            return True
        return False

    async def get_recent_activity(self, limit: int = 5) -> List[dict]:
        """
        Derives recent activity from JobProfile records.
        Returns the latest 'limit' profiles formatted as activity.
        """
        query = select(JobProfile).order_by(JobProfile.created_at.desc()).limit(limit)
        result = await self.async_session.execute(query)
        profiles = result.scalars().all()
        
        activities = []
        for p in profiles:
            activities.append({
                "id": p.id,
                "title": p.job_name,
                "action": "created",
                "message": f"Role '{p.job_name}' was created",
                "createdAt": p.created_at
            })
        return activities
