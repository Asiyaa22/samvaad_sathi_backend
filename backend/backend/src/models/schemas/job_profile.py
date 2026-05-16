from pydantic import BaseModel
from typing import List, Optional
import datetime

class JobProfileBase(BaseModel):
    title: str
    description: Optional[str] = None

class JobProfileCreate(JobProfileBase):
    pass

class JobProfileResponse(JobProfileBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class JobProfileSummaryResponse(BaseModel):
    totalRoles: int
    pendingReview: int
    approved: int
    rejected: int

class JobProfileListResponse(BaseModel):
    items: List[JobProfileResponse]
    total: int

class JobProfileActivityResponse(BaseModel):
    id: int
    title: str
    action: str
    message: str
    createdAt: datetime.datetime

class JobProfileUploadResponse(BaseModel):
    success: bool
    originalFileName: str
    storedFileName: str
    fileType: str
    fileSize: int
    filePath: str

class JobProfileExtractSkillsRequest(BaseModel):
    jobDescription: str

class JobProfileExtractSkillsResponse(BaseModel):
    skills: List[str]
