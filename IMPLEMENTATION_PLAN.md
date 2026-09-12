# TURMERIC SHIELD — IMPLEMENTATION PLAN

## 1. Current Prototype — Working Foundation

- FastAPI + Python transparent rule engine accepts **structured** field, weather-context, crop-context and local-history inputs.
- The current engine produces an explainable **Risk Priority**, contributing evidence, recommended action and next step.
- Streamlit demonstrates the farmer/field-worker workflow.
- Optional visual evidence is represented as a supporting structured input; **an image model is not executed in the current prototype**.

## 2. Turmeric Shield Risk-Fusion Layer

**Inputs:** weather context, field condition, crop context, local history, optional visual evidence.

**Analysis dimensions:** environmental, temporal, spatial, crop-context and visual.

**Output:** HIGH / MODERATE / LOW / UNCERTAIN.

- HIGH → prioritize field inspection + expert validation.
- MODERATE → inspect + preventive/IPM action.
- LOW → continue monitoring.
- UNCERTAIN → collect additional evidence and use expert/lab referral where needed.

Current weights and thresholds are **illustrative MVP assumptions**, not scientifically validated disease thresholds.

## 3. Field Validation — Primary Path: Turmeric

- Independently seek legitimate turmeric-field access through agriculture contacts, farmers, institutions, mentors or other field connections; the project should not depend on a single referral.
- Collect timestamped environmental/field observations with crop stage, drainage, rainfall/moisture trends, symptoms and local context.
- Where naturally occurring suspected/healthy cases are available, document field observations and expert/field-officer observations where possible.
- Compare risk priorities with later field observations, document false positives/false negatives, and refine the transparent rules.
- A baseline field deployment can validate sensing, data collection and workflow, but a confirmed disease case is required before making disease-performance claims.

## 4. Contingency Validation — If Turmeric Access Is Unavailable

- Use another suitable crop/plant only for **engineering proof-of-concept**: sensing/data collection, API integration, explainable risk fusion, logging and field workflow.
- Do **not** transfer another crop's thresholds or validation results to turmeric.
- Turmeric-specific disease claims remain unvalidated until turmeric observations and appropriate expert confirmation are obtained.

## 5. Scale-Up Roadmap

### Phase 2 — Field Expansion
- Raspberry Pi / IoT sensing
- GIS hotspot mapping
- multilingual / voice interface
- broader field coverage

### Phase 3 — Validation & Scale
- expert-confirmed labelled dataset
- calibrated/validated ML forecasting
- institutional/government integration
- extension-worker dashboard
- live weather and image-model integrations

## 6. Technology & Deliverable

**Current:** Python, FastAPI, Streamlit, structured context data, CSV/SQLite-compatible data layer, explainable rule engine.

**Future:** live weather ingestion, multimodal image inference, Raspberry Pi/IoT, GIS and validated ML.

**Deliverable:** a working prototype that prioritizes fields for inspection, exposes the evidence behind each priority, documents uncertainty, and provides a realistic route from prototype → field validation → validated forecasting.
