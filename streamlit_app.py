import requests
import streamlit as st

st.set_page_config(
    page_title="Turmeric Shield",
    page_icon="🌱",
    layout="wide",
)

st.title("🌱 Turmeric Shield")
st.caption(
    "Explainable early-warning & decision support for turmeric rhizome-rot risk"
)
st.info(
    "Current prototype: structured inputs + transparent rule engine. "
    "Risk priority is not disease diagnosis. Thresholds are illustrative "
    "and require field/expert validation."
)

with st.sidebar:
    st.header("Field / Crop Input")

    farmer_name = st.text_input("Farmer / Field", "Demo Field")
    crop_stage = st.text_input("Crop stage", "Rhizome development")
    variety = st.text_input("Variety", "")
    moisture = st.slider("Soil moisture (%)", 0, 100, 75)
    drainage = st.selectbox(
        "Drainage",
        ["good", "moderate", "poor"],
        index=1,
    )

    st.subheader("Weather / Temporal Context")
    st.caption(
        "Structured prototype inputs. Live weather API ingestion is a future integration."
    )
    temperature = st.number_input("Temperature (°C)", value=28.0)
    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0,
    )
    rainfall = st.number_input(
        "Recent rainfall (mm)",
        min_value=0.0,
        value=40.0,
    )
    rainfall_trend = st.selectbox(
        "Rainfall trend",
        ["decreasing", "stable", "increasing"],
        index=1,
    )
    moisture_trend = st.selectbox(
        "Moisture trend",
        ["decreasing", "stable", "increasing"],
        index=2,
    )

    st.subheader("Spatial / Local History")
    nearby_cases = st.number_input(
        "Nearby cases — last 14 days",
        min_value=0,
        value=1,
        step=1,
    )
    case_trend = st.selectbox(
        "Nearby-case trend",
        ["decreasing", "stable", "increasing"],
        index=1,
    )

  st.subheader("Manual Visual Evidence — Prototype")
st.caption(
    "Manual observation only. No image model is executed here yet; "
    "actual multimodal inference is a future integration."
)
visual = st.selectbox(
    "Manual visual observation",
        [
            "not_available",
            "supportive",
            "not_supportive",
            "uncertain",
        ],
        help=(
            "This field records supporting visual evidence only. "
            "Multimodal image inference is a future integration."
        ),
    )

    run = st.button(
        "Assess Risk",
        type="primary",
        use_container_width=True,
    )

if run:
    payload = {
        "farmer_name": farmer_name,
        "crop_name": "turmeric",
        "soil_moisture_percentage": moisture,
        "drainage": drainage,
        "temperature_c": temperature,
        "humidity_percentage": humidity,
        "recent_rainfall_mm": rainfall,
        "rainfall_trend": rainfall_trend,
        "moisture_trend": moisture_trend,
        "crop_stage": crop_stage or None,
        "variety": variety or None,
        "nearby_cases_last_14_days": int(nearby_cases),
        "nearby_case_trend": case_trend,
        "visual_assessment": visual,
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/check-risk",
            json=payload,
            timeout=5,
        )
        response.raise_for_status()
        result = response.json()

        c1, c2, c3 = st.columns(3)
        c1.metric("Risk Priority", result["risk_priority"])
        c2.metric("Prototype Score", result["priority_score"])
      c3.metric("Context Completeness", result["context_completeness"])

        st.subheader("Recommended Action")
        st.success(result["action"])

        st.subheader("Next Step")
        st.write(result["next_step"])

        st.subheader("Explainable Evidence")
        for item in result["evidence"]:
            st.write(
                f"**{item['category']} — {item['signal']}** "
                f"(+{item['contribution']}) — {item['interpretation']}"
            )

        if result["missing_or_uncertain"]:
            st.warning(
                "Missing / uncertain context: "
                + ", ".join(result["missing_or_uncertain"])
            )

        with st.expander("API response"):
            st.json(result)

    except requests.RequestException:
        st.error(
            "FastAPI backend is not running. Start it with: "
            "`uvicorn main:app --reload`"
        )
else:
    st.subheader("Current prototype workflow")
    st.write("Monitor → Assess → Prioritize → Act → Verify → Learn")
    st.write(
        "Structured weather context + field condition + crop context + "
        "local history + optional supporting visual evidence are combined "
        "by a transparent Python rule engine."
    )
    st.caption(
        "Future integrations: live weather ingestion, image-model inference, "
        "IoT/Raspberry Pi sensing, GIS and validated ML forecasting."
    )
