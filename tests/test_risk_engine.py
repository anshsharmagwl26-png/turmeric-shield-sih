from models import CropRiskInput
from risk_engine import assess_risk


def base_input(**overrides):
    data = {
        "farmer_name": "Test Farmer",
        "crop_name": "turmeric",
        "soil_moisture_percentage": 75,
        "drainage": "moderate",
        "temperature_c": 28,
        "humidity_percentage": 80,
        "recent_rainfall_mm": 40,
        "rainfall_trend": "stable",
        "moisture_trend": "stable",
        "crop_stage": "rhizome development",
        "variety": "test",
        "nearby_cases_last_14_days": 1,
        "nearby_case_trend": "stable",
        "visual_assessment": "not_available",
    }
    data.update(overrides)
    return CropRiskInput(**data)


def test_high_priority_from_multiple_signals():
    result = assess_risk(
        base_input(
            soil_moisture_percentage=85,
            drainage="poor",
            recent_rainfall_mm=60,
            rainfall_trend="increasing",
            moisture_trend="increasing",
            humidity_percentage=88,
            nearby_cases_last_14_days=3,
            nearby_case_trend="increasing",
        )
    )

    assert result["risk_priority"] == "HIGH"
    assert result["priority_score"] >= 10


def test_uncertain_when_context_is_insufficient():
    result = assess_risk(
        base_input(
            soil_moisture_percentage=40,
            drainage="good",
            recent_rainfall_mm=None,
            temperature_c=None,
            humidity_percentage=None,
            crop_stage=None,
            variety=None,
            nearby_cases_last_14_days=0,
            visual_assessment="not_available",
        )
    )

    assert result["risk_priority"] == "UNCERTAIN"
    assert len(result["missing_or_uncertain"]) >= 3


def test_crop_context_is_recorded_not_weighted():
    result = assess_risk(
        base_input(
            crop_stage="early growth",
            variety="variety-a",
        )
    )

    crop_items = [
        item for item in result["evidence"]
        if item["category"] == "Crop context"
    ]

    assert crop_items
    assert all(item["contribution"] == 0 for item in crop_items)


def test_visual_assessment_is_recorded_without_current_score_change():
    without_visual = assess_risk(
        base_input(visual_assessment="not_available")
    )
    with_visual = assess_risk(
        base_input(visual_assessment="supportive")
    )

    assert with_visual["priority_score"] == without_visual["priority_score"]
    assert any(
        item["category"] == "Visual"
        for item in with_visual["evidence"]
    )
