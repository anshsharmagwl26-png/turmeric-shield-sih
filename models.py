from typing import List, Literal, Optional

from pydantic import BaseModel, Field


Drainage = Literal["good", "moderate", "poor"]
Trend = Literal["decreasing", "stable", "increasing"]
VisualStatus = Literal[
    "not_available",
    "supportive",
    "not_supportive",
    "uncertain",
]


class CropRiskInput(BaseModel):
    farmer_name: str
    crop_name: str = "turmeric"

    # Field condition
    soil_moisture_percentage: float = Field(..., ge=0, le=100)
    drainage: Drainage = "moderate"

    # Weather / temporal context
    # These are structured inputs in the current prototype.
    temperature_c: Optional[float] = Field(None, ge=-20, le=60)
    humidity_percentage: Optional[float] = Field(None, ge=0, le=100)
    recent_rainfall_mm: Optional[float] = Field(None, ge=0)
    rainfall_trend: Trend = "stable"
    moisture_trend: Trend = "stable"

    # Crop context
    crop_stage: Optional[str] = None
    variety: Optional[str] = None

    # Spatial / local history
    nearby_cases_last_14_days: int = Field(0, ge=0)
    nearby_case_trend: Trend = "stable"

    # Current prototype representation of optional visual evidence.
    # This is NOT an integrated image/vision model.
    visual_assessment: VisualStatus = "not_available"


class EvidenceItem(BaseModel):
    category: str
    signal: str
    contribution: int
    interpretation: str


class RiskResult(BaseModel):
    project: str
    crop: str
    farmer: str
    risk_priority: str
    priority_score: int
    evidence_strength: str
    action: str
    next_step: str
    evidence: List[EvidenceItem]
    missing_or_uncertain: List[str]
    disclaimer: str
