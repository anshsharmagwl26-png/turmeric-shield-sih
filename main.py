from fastapi import FastAPI
from models import CropRiskInput
from risk_engine import assess_risk

app = FastAPI(
    title="Turmeric Shield API",
    description=(
        "Prototype explainable early-warning and decision-support API "
        "for turmeric rhizome-rot risk prioritization."
    ),
    version="1.0.0-prototype",
)


@app.get("/")
def root():
    return {
        "project": "Turmeric Shield",
        "status": "prototype",
        "workflow": "Monitor -> Assess -> Prioritize -> Act -> Verify -> Learn",
        "current_implementation": [
            "FastAPI backend",
            "transparent Python rule engine",
            "structured field/weather-context/crop-context/local-history inputs",
            "explainable evidence output",
        ],
        "not_yet_implemented": [
            "live weather API ingestion",
            "multimodal image inference",
            "IoT/Raspberry Pi sensing",
            "validated ML forecasting",
        ],
        "disclaimer": (
            "Risk prioritization only; not a confirmed disease diagnosis. "
            "Prototype weights and thresholds require field/expert validation."
        ),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/check-risk")
def check_risk(data: CropRiskInput):
    return assess_risk(data)


# Keeps the original demo endpoint usable.
@app.post("/check-crop")
def check_crop(data: CropRiskInput):
    return assess_risk(data)
