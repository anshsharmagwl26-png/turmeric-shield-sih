from models import CropRiskInput, EvidenceItem


def _evidence(
    category: str,
    signal: str,
    contribution: int,
    interpretation: str,
) -> EvidenceItem:
    return EvidenceItem(
        category=category,
        signal=signal,
        contribution=contribution,
        interpretation=interpretation,
    )


def assess_risk(data: CropRiskInput) -> dict:
    """
    Transparent prototype rule engine.

    The current score is intentionally simple and inspectable.

    IMPORTANT:
    - Thresholds and weights are illustrative MVP assumptions.
    - They are not scientifically validated disease thresholds.
    - The engine prioritizes inspection; it does not diagnose disease.
    - Crop stage and variety are currently captured as context but do not
      yet change the numerical score.
    - "visual_assessment" is a structured supporting input, not an image
      inference model.
    """

    score = 0
    evidence = []
    missing = []

    # ------------------------------------------------------------------
    # 1. Environmental / field condition
    # ------------------------------------------------------------------
    if data.soil_moisture_percentage >= 80:
        score += 3
        evidence.append(
            _evidence(
                "Environmental",
                "Soil moisture",
                3,
                "High soil moisture adds a stronger field-condition signal "
                "for inspection priority.",
            )
        )
    elif data.soil_moisture_percentage >= 65:
        score += 2
        evidence.append(
            _evidence(
                "Environmental",
                "Soil moisture",
                2,
                "Elevated soil moisture adds a moderate field-condition signal.",
            )
        )
    else:
        evidence.append(
            _evidence(
                "Environmental",
                "Soil moisture",
                0,
                "No elevated moisture signal from the configured prototype rule.",
            )
        )

    if data.drainage == "poor":
        score += 3
        evidence.append(
            _evidence(
                "Environmental",
                "Drainage",
                3,
                "Poor drainage strengthens the moisture-related inspection signal.",
            )
        )
    elif data.drainage == "moderate":
        score += 1
        evidence.append(
            _evidence(
                "Environmental",
                "Drainage",
                1,
                "Moderate drainage adds a smaller field-condition signal.",
            )
        )
    else:
        evidence.append(
            _evidence(
                "Environmental",
                "Drainage",
                0,
                "Good drainage does not add risk in this prototype rule set.",
            )
        )

    # ------------------------------------------------------------------
    # 2. Weather / temporal context
    # ------------------------------------------------------------------
    if data.recent_rainfall_mm is None:
        missing.append("Recent rainfall")
    elif data.recent_rainfall_mm >= 50:
        score += 3
        evidence.append(
            _evidence(
                "Temporal",
                "Recent rainfall",
                3,
                "Higher recent rainfall strengthens the wet-field contextual signal.",
            )
        )
    elif data.recent_rainfall_mm >= 25:
        score += 1
        evidence.append(
            _evidence(
                "Temporal",
                "Recent rainfall",
                1,
                "Recent rainfall adds a moderate contextual signal.",
            )
        )
    else:
        evidence.append(
            _evidence(
                "Temporal",
                "Recent rainfall",
                0,
                "No elevated rainfall signal from the configured prototype rule.",
            )
        )

    if data.rainfall_trend == "increasing":
        score += 1
        evidence.append(
            _evidence(
                "Temporal",
                "Rainfall trend",
                1,
                "Increasing rainfall trend adds temporal context.",
            )
        )

    if data.moisture_trend == "increasing":
        score += 1
        evidence.append(
            _evidence(
                "Temporal",
                "Soil-moisture trend",
                1,
                "Increasing moisture trend adds temporal context.",
            )
        )

    if data.humidity_percentage is None:
        missing.append("Humidity")
    elif data.humidity_percentage >= 85:
        score += 1
        evidence.append(
            _evidence(
                "Environmental",
                "Humidity",
                1,
                "High humidity adds supporting environmental context.",
            )
        )

    if data.temperature_c is None:
        missing.append("Temperature")

    # ------------------------------------------------------------------
    # 3. Spatial / local history
    # ------------------------------------------------------------------
    if data.nearby_cases_last_14_days >= 3:
        score += 3
        evidence.append(
            _evidence(
                "Spatial",
                "Nearby recent cases",
                3,
                "Multiple nearby recent cases strengthen the local-case signal.",
            )
        )
    elif data.nearby_cases_last_14_days > 0:
        score += 2
        evidence.append(
            _evidence(
                "Spatial",
                "Nearby recent cases",
                2,
                "Recent nearby cases add local spatial context.",
            )
        )
    else:
        evidence.append(
            _evidence(
                "Spatial",
                "Nearby recent cases",
                0,
                "No nearby cases were supplied for this prototype assessment.",
            )
        )

    if data.nearby_case_trend == "increasing":
        score += 1
        evidence.append(
            _evidence(
                "Spatial",
                "Nearby-case trend",
                1,
                "Increasing nearby-case trend adds local temporal context.",
            )
        )

    # ------------------------------------------------------------------
    # 4. Crop context
    # ------------------------------------------------------------------
    if not data.crop_stage:
        missing.append("Crop stage")
    else:
        evidence.append(
            _evidence(
                "Crop context",
                "Crop stage",
                0,
                f"Crop stage recorded as '{data.crop_stage}'. "
                "Stage-specific weighting is reserved for future calibration.",
            )
        )

    if not data.variety:
        missing.append("Variety")
    else:
        evidence.append(
            _evidence(
                "Crop context",
                "Variety",
                0,
                f"Variety recorded as '{data.variety}'. "
                "Variety-specific weighting is reserved for future calibration.",
            )
        )

    # ------------------------------------------------------------------
    # 5. Optional visual evidence
    # ------------------------------------------------------------------
    # This is a structured prototype input only.
    if data.visual_assessment == "supportive":
        score += 2
        evidence.append(
            _evidence(
                "Visual",
                "Supporting symptom assessment",
                2,
                "A supporting visual assessment adds additional evidence. "
                "This value is not produced by an integrated image model yet.",
            )
        )
    elif data.visual_assessment == "uncertain":
        missing.append("Visual assessment is uncertain")
        evidence.append(
            _evidence(
                "Visual",
                "Uncertain visual assessment",
                0,
                "Visual evidence is inconclusive and must not be treated as diagnosis.",
            )
        )
    elif data.visual_assessment == "not_available":
        missing.append("Optional visual assessment")
    else:
        evidence.append(
            _evidence(
                "Visual",
                "No supportive visual signal",
                0,
                "No additional visual risk contribution was supplied.",
            )
        )

    # ------------------------------------------------------------------
    # 6. Current priority logic
    # ------------------------------------------------------------------
    # UNCERTAIN is currently used when the available evidence is too
    # incomplete to justify a stronger priority, not as a generic
    # "conflicting signals" detector.
    if score >= 10:
        priority = "HIGH"
        action = "Prioritize field inspection and expert validation."
        next_step = (
            "Inspect the field first, document observations, and seek "
            "expert/field-officer confirmation."
        )
    elif score >= 6:
        priority = "MODERATE"
        action = "Inspect the field and consider preventive/IPM measures."
        next_step = (
            "Schedule inspection and review moisture, drainage and "
            "recent local trends."
        )
    elif score <= 2 and len(missing) >= 3:
        priority = "UNCERTAIN"
        action = (
            "Collect additional evidence and use expert/lab referral "
            "where needed."
        )
        next_step = (
            "Collect missing field/context information before making "
            "a stronger priority decision."
        )
    else:
        priority = "LOW"
        action = "Continue monitoring field conditions."
        next_step = (
            "Continue monitoring and update the assessment when new "
            "observations arrive."
        )

    # This describes input completeness, not model accuracy.
    if len(missing) == 0:
        evidence_strength = "STRONGER-CONTEXT"
    elif len(missing) <= 2:
        evidence_strength = "PARTIAL-CONTEXT"
    else:
        evidence_strength = "LIMITED-CONTEXT"

    return {
        "project": "Turmeric Shield",
        "crop": data.crop_name,
        "farmer": data.farmer_name,
        "risk_priority": priority,
        "priority_score": score,
        "evidence_strength": evidence_strength,
        "action": action,
        "next_step": next_step,
        "evidence": [item.model_dump() for item in evidence],
        "missing_or_uncertain": missing,
        "disclaimer": (
            "Prototype risk prioritization only. Current rule weights and "
            "thresholds are illustrative and require field/expert validation. "
            "The system does not provide confirmed disease diagnosis."
        ),
    }
