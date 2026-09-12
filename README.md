# 🌱 Turmeric Shield

## Explainable Early-Warning & Decision Support for Turmeric Rhizome Rot

**Smart India Hackathon 2026 — SIH26131**  
**Team: Code4cause**

Turmeric Shield is a prototype decision-support system designed around one principle:

> **Risk first → supporting assessment second → targeted action → expert validation**

The concept brings together field conditions, weather context, crop context and local case patterns so that risky fields can be **prioritized for inspection** rather than waiting only for severe visible damage.

---

## 🔄 Core workflow

**Monitor → Assess → Prioritize → Act → Verify → Learn**

```text
  Structured weather context ───┐
  Field condition ──────────────┤
  Crop context ─────────────────┤
  Local history ────────────────┤
  Optional visual evidence ─────┤
                                ▼
                       ┌──────────────────┐
                       │ Explainable      │
                       │ Python Rule      │
                       │ Risk Engine      │
                       └────────┬─────────┘
                                ▼
                ┌───────────────┼────────────────┐
                ▼               ▼                ▼
              HIGH           MODERATE           LOW
          inspect +        inspect +         continue
           expert           preventive/       monitoring
          validation        IPM action
                │
                ▼
           UNCERTAIN
      additional evidence /
        expert-lab referral
```

---

## 🧩 What is actually implemented

This repository contains a **working prototype**, not a claim that the complete field system is already deployed.

### Current working components

- FastAPI backend
- Python transparent rule engine
- Streamlit dashboard
- Structured field-condition inputs
- Structured weather-context inputs
- Structured crop-context inputs
- Structured local-history/spatial inputs
- Explainable evidence contributions
- HIGH / MODERATE / LOW / UNCERTAIN priorities
- Recommended action + next step
- Missing/uncertain information reporting
- Basic automated tests
- Sample case-history data

### Not yet implemented

- Live weather API ingestion
- Actual image upload + multimodal model inference
- Raspberry Pi / IoT field sensing
- GIS hotspot mapping
- Expert-confirmed labelled dataset
- Validated ML forecasting
- Government/institutional production integration

Those are implementation/scale-up stages rather than features being falsely represented as complete.

---

## 🧠 Evidence model

| Evidence source | Current representation | Contribution today |
|---|---|---|
| Environmental | soil moisture, drainage, humidity | contributes to prototype score |
| Temporal | recent rainfall, rainfall trend, moisture trend | contributes to prototype score |
| Crop context | crop stage, variety | recorded as context; **not yet weighted** |
| Spatial | nearby cases + local trend | contributes to prototype score |
| Visual | manual structured observation | recorded as supporting context; not produced by an image model and not weighted yet |

### Important distinction

**Weather is currently a structured input, not a live API feed.**

**Visual assessment is currently a structured supporting input, not a running multimodal AI model.**
**Temperature is currently captured as contextual data but is not weighted in the prototype score.**

This keeps the repository aligned with the actual implementation.

---

## ⚙️ How the current rule engine works

The current prototype uses a transparent **weighted additive score**.

Illustrative examples:

- soil moisture ≥ 80% → +3
- soil moisture 65–79% → +2
- poor drainage → +3
- moderate drainage → +1
- recent rainfall ≥ 50 mm → +3
- recent rainfall 25–49 mm → +1
- increasing rainfall trend → +1
- increasing moisture trend → +1
- humidity ≥ 85% → +1
- nearby cases ≥ 3 → +3
- nearby cases 1–2 → +2
- increasing nearby-case trend → +1
- - visual observation → recorded as supporting context; no score contribution in the current prototype

Current priority mapping:

```text
10+       → HIGH
6–9       → MODERATE
≤2 + ≥3 missing context items
          → UNCERTAIN
otherwise → LOW
```

### What these numbers mean

They are **illustrative prototype weights and thresholds** used to make the decision path transparent.

They are **not scientifically validated disease thresholds**.

They must be calibrated against real field observations and appropriate expert confirmation before disease-performance claims are made.

---

## 🔎 Why the engine is explainable

For each assessment, the API returns:

- prototype priority score
- HIGH / MODERATE / LOW / UNCERTAIN
- - context completeness
- each contributing signal
- contribution of each signal
- interpretation of that signal
- recommended action
- next step
- missing or uncertain information
- validation disclaimer

So the output is not a black-box label such as “HIGH”.

The intended question is:

> **“Why was this field prioritized?”**

The prototype can show which available signals contributed to that priority.

---

## 🟡 What UNCERTAIN means in the current prototype

The current implementation does **not** claim to detect conflicting signals as a general contradiction engine.

In this prototype, **UNCERTAIN** is used when the available context is too incomplete to justify a stronger priority decision.

The next action is to collect more evidence and/or use expert/lab referral where appropriate.

A future calibrated system may incorporate more sophisticated evidence-conflict handling.

---

## 🌾 Crop context and future calibration

Crop stage and variety are accepted and recorded because they are important contextual variables.

However, **the current prototype does not change the numerical score based on crop stage or variety**.

Stage-specific and variety-specific weighting is intentionally deferred until field observations and expert-confirmed outcomes are available.

This prevents the repository from pretending that unvalidated stage-specific thresholds are already established.

---

## 👁️ Visual assessment

The architecture allows optional visual evidence when visible symptoms are available.

In this repository, `visual_assessment` is a **structured prototype input**:

- `not_available`
- `supportive`
- `not_supportive`
- `uncertain`

It is **not** an actual image-analysis model.

A future multimodal integration can replace this structured field with an image pipeline while preserving the same safety boundary:

> **supporting assessment, not confirmed diagnosis**

---

## 🧪 Field validation plan

The primary validation target is **turmeric**.

The team will independently seek legitimate field access through agriculture contacts, farmers, institutions, mentors and other field connections; the project does not depend on a single referral.

For each observation, the target data record includes:

1. timestamp
2. soil/environmental readings
3. crop stage
4. drainage/field condition
5. recent rainfall and moisture trends
6. observed symptoms
7. nearby/local case context
8. expert or field-officer observations where available

The team can then compare **risk priorities** with later field observations, document false positives/false negatives, and calibrate the transparent rules.

A field deployment that only collects baseline sensor/context data can demonstrate the sensing/data-collection and workflow pipeline. It does **not** by itself establish turmeric disease-detection performance.

### Contingency

If turmeric-field access is temporarily unavailable, another suitable crop/plant may be used for an **engineering proof-of-concept** of:

- sensing/data collection
- API integration
- explainable rule fusion
- logging
- field-user workflow

Results or thresholds from another crop will **not** be transferred to turmeric.

---

## 🤖 Why not ML first?

A predictive model requires a sufficiently reliable expert-confirmed labelled dataset.

The intended path is:

**collect data → confirm observations → calibrate rules → evaluate false positives/false negatives → build labelled dataset → validate ML forecasting**

This is intended to avoid introducing a model that gives a misleading appearance of precision without appropriate ground truth.

---

## 🛣️ Scale-up roadmap

### Phase 2 — Field Expansion

- Raspberry Pi / IoT sensing
- GIS hotspot mapping
- multilingual / voice interface
- broader field coverage
- live weather ingestion

### Phase 3 — Validation & Scale

- expert-confirmed labelled dataset
- calibrated/validated ML forecasting
- multimodal image inference
- institutional/government integration
- extension-worker dashboard

---

## ▶️ Run locally

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Start FastAPI

```bash
uvicorn main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Start Streamlit

Open a second terminal:

```bash
streamlit run streamlit_app.py
```

The dashboard connects to the local FastAPI backend.

---

## 🔌 Example request

A ready-to-use example is available at:

```text
data/demo_request.json
```

You can also test the API using `/docs`.

---

## 🧪 Tests

Run:

```bash
pytest
```

The tests currently cover:

- high-priority multi-signal assessment
- insufficient-context → UNCERTAIN behavior
- crop-context recording without false stage weighting
- supporting visual input behavior

---

## 📁 Repository structure

```text
TurmericShield/
├── main.py
├── models.py
├── risk_engine.py
├── streamlit_app.py
├── requirements.txt
├── README.md
├── IMPLEMENTATION_PLAN.md
├── .gitignore
├── data/
│   ├── demo_request.json
│   └── sample_cases.csv
└── tests/
    └── test_risk_engine.py
```

---

## ⚠️ Current limitations

- Prototype thresholds and weights are illustrative.
- No expert-confirmed local disease dataset is included yet.
- Weather is structured input rather than a live weather API.
- Visual evidence is a manual structured observation rather than running image inference, and it is not currently weighted.
- IoT is a future field-expansion component.
- Crop stage and variety are recorded but not yet used as numerical weighting factors.
- No validated disease-detection accuracy figure is claimed.
- The system does not provide confirmed pathogen/disease diagnosis.

---

## 📌 Project status

**Prototype / SIH 2026 implementation stage**

**Code4cause**  
**Problem Statement:** SIH26131 — Early detection and management of crop diseases and pest infestations

> **Risk identification → supporting assessment → targeted action → expert validation → learning**
