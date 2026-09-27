from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CreatorProfile(BaseModel):
    name: str = ""
    role: str = ""
    skills: List[str] = Field(default_factory=list)
    experience: str = ""
    interests: List[str] = Field(default_factory=list)
    goals: str = ""
    platforms: List[str] = Field(default_factory=list)
    audience_hint: str = ""
    existing_content: str = ""
    location: str = ""
    preferred_style: str = ""


class BuildRequest(BaseModel):
    profile: CreatorProfile


class ImproveRequest(BaseModel):
    project: Dict[str, Any]


class ImageRequest(BaseModel):
    project: Dict[str, Any]
