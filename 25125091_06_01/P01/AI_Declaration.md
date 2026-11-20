# AI Usage Declaration

> **Course:** CS252 – Computational Thinking  
> **Assignment:** Lab 06 – OpenStreetMap API & OpenWeather/Hydrology Integration  
> **Submission Type:** Individual Contribution to Course Group Project (SmartRoute - Group 06)  
> **Student Name:** Tran Duc Toan (Trần Đức Toàn)  
> **Student ID:** 25125091 | **Class:** 25A01  

---

## 1. AI Tooling & Environment
* **Primary AI Engine:** Google Antigravity Assistant (powered by Gemini 3.8 Flash).
* **Work Environment:** Interactive pair-programming directly within the local workspace environment.

---

## 2. Phased Scope of AI Collaboration (Spec-Driven Workflow)

The collaboration with the AI assistant followed structured, phased software engineering methodologies:

1. **Reconnaissance & OpenStreetMap / Weather API Contract Analysis:**
   * Analyzed OpenStreetMap network structures extracted via OSMnx for Bình Thạnh District, examining signalized junction tags (`highway=traffic_signals`) and edge coordinate geometries.
   * Assessed environmental telemetry ingestion pipelines connecting rain radar and Phú An tide-gauge hydrographs with in-memory dynamic overlay grids.
2. **Interface Contract & Architecture Design:**
   * Formulated and reviewed formal API function signatures:
     - `get_major_intersection_delay(name: str) -> float` with multi-stage alias normalization.
     - `format_eta_breakdown(driving_time_s, intersections) -> dict` decomposing $\text{ETA} = \text{Driving} + \text{Webster Delays}$.
     - `generate_web_speech_script(text, rate) -> str` generating ready-to-inject browser Web Speech API JavaScript.
3. **Code Implementation & Integration:**
   * Expanded Webster traffic delay logic (`src/signals/webster.py`) with calibrated empirical lookup parameters for 3 major Bình Thạnh intersections (Hàng Xanh, D2–D5, Đinh Bộ Lĩnh).
   * Developed Web Speech API voice alert integration (`src/alerts/voice.py`) emitting natural Vietnamese speech prompts.
   * Implemented geodetic Haversine distance calculations and look-ahead proximity hazard scanning algorithms.
4. **Documentation & Architectural Artifacts:**
   * Formatted and rendered Mermaid architectural flowcharts, sequence diagrams, and mathematical formulations for the comprehensive development report.

---

## 3. Human Oversight & Engineering Verification

* **Mathematical Verification:** The student independently audited Webster's equation $E[\text{wait}] = \frac{R^2}{2(R+G)}$, verified the calibrated values for Bình Thạnh intersections against urban signal timings, and ensured consistent decomposition of ETA.
* **Deontic Constraint Enforcement:** The student strictly inspected safety boundaries, ensuring that water depth exceeding ground clearance ($H_{\text{water}} > H_{\text{safe}}$) results in infinite edge cost ($W = +\infty$) and immediate failover rerouting.
* **Live Integration & End-to-End Verification:** The student merged upstream branches (`origin/demo`), verified Web Speech API synthesis in modern browsers, and tested the live navigation simulation puck on the OpenStreetMap visualizer.
