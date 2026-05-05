from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field


class Audience(BaseModel):
    description: str = ""
    segments: List[str] = Field(default_factory=list)
    source: str = ""


class MessagingPillar(BaseModel):
    pillar: str = ""
    variants: List[str] = Field(default_factory=list)


class Messaging(BaseModel):
    pillars: List[MessagingPillar] = Field(default_factory=list)
    tone: str = ""


class ChannelPlan(BaseModel):
    type: str = ""
    strategy: str = ""
    assets: List[str] = Field(default_factory=list)


class Creative(BaseModel):
    concepts: List[str] = Field(default_factory=list)
    assets: List[str] = Field(default_factory=list)
    status: str = "draft"


class Operations(BaseModel):
    budget: str = ""
    timeline: str = ""
    campaign_name: str = ""
    requirements: List[str] = Field(default_factory=list)


class Governance(BaseModel):
    checks_passed: bool = False
    issues: List[str] = Field(default_factory=list)


class Outputs(BaseModel):
    confluence_url: str = ""
    asana_project_id: str = ""


class Metadata(BaseModel):
    created_by: str = ""
    last_updated: str = ""


class Campaign(BaseModel):
    id: str = ""
    name: str = ""
    objective: str = ""
    audience: Audience = Field(default_factory=Audience)
    messaging: Messaging = Field(default_factory=Messaging)
    channels: List[ChannelPlan] = Field(default_factory=list)
    creative: Creative = Field(default_factory=Creative)
    operations: Operations = Field(default_factory=Operations)
    governance: Governance = Field(default_factory=Governance)
    outputs: Outputs = Field(default_factory=Outputs)
    metadata: Metadata = Field(default_factory=Metadata)
