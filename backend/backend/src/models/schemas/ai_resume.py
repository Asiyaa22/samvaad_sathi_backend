from pydantic import BaseModel
from typing import List, Optional


class ScoreBreakdown(BaseModel):
    skillsMatch: int
    experienceMatch: int
    formattingScore: int
    keywordDensity: int


class SkillsAnalysis(BaseModel):
    strongSkills: List[str]
    missingSkills: List[str]
    deprioritizedSkills: List[str]


class ProjectFeedbackItem(BaseModel):
    projectName: str
    rating: str
    feedback: str


class HygieneCheck(BaseModel):
    grammarIssues: List[str]
    hasLinkedIn: bool
    hasGithub: bool
    hasPortfolio: bool


class ResumeAnalysisResponse(BaseModel):
    analysisId: str
    atsScore: int
    summary: str
    scoreBreakdown: ScoreBreakdown
    skillsAnalysis: SkillsAnalysis
    projectFeedback: List[ProjectFeedbackItem]
    projectRecommendations: List[str]
    hygieneCheck: HygieneCheck