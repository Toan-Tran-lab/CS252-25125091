# Lab 06: OpenStreetMap API & Weather/Hydrology Integration

> **Course:** CS252 – Computational Thinking, Class 25A01  
> **Student:** Tran Duc Toan (Trần Đức Toàn)  
> **Student ID:** 25125091  
> **Group Project:** SmartRoute — Urban Inundation Routing & Hazard Alert System (Group 06)  
> **Submission Track:** Alternative Option — Individual Contribution (at least 1 product feature) to Group Project  

---

## 1. Feature Description & OpenStreetMap / Weather API Integration

### 1.1. Feature Overview
This submission presents the individual product feature developed by **Tran Duc Toan (25125091)** for the **SmartRoute** course project (Group 06):
* **Webster (1958) Traffic Signal Delay Modeling:** Analytical stochastic modeling of delay at signalized road junctions across 3 Computational Thinking iterations (V1 Constant $\to$ V2 Uniform Arrival $\to$ V3 Context-Aware Congestion Factor) and calibrated empirical lookup parameters for 3 major Bình Thạnh intersections (Hàng Xanh, D2–D5, Đinh Bộ Lĩnh).
* **Real-time Proximity Hazard Alerting & Vietnamese Web Speech API Synthesis:** Look-ahead route proximity scanner evaluating vehicle-specific Deontic safety constraints ($H_{\text{water}} > H_{\text{safe}} \implies \text{CRITICAL}$ / failover reroute) and triggering multi-modal alerts (audio chime, mobile haptic vibration, visual flashing banners, and natural Vietnamese speech synthesis via browser Web Speech API: `"Chú ý: Phía trước có điểm ngập nước / ổ gà, vui lòng giảm tốc độ"`).

### 1.2. How OpenStreetMap (OSM) & Weather Data are Integrated
1. **OpenStreetMap Road Network:** The physical street topology of Bình Thạnh District is extracted via `OSMnx` into an immutable directed multigraph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$. Signalized junction nodes with OpenStreetMap tags (`highway=traffic_signals`) are dynamically linked with Webster delay models, and route coordinates are parsed to calculate real-time Haversine geodetic distances.
2. **Weather & Hydrological Data:** Real-time tidal gauge readings from the Saigon River (Phú An hydrographic station) and rainfall radar intensities are transformed into water depth surfaces $H(e, t)$ and stored in an in-memory hash map (`InMemoryDeltaOverlay`), enabling instant vehicle clearance evaluation.
3. **Interactive Web Demonstration:** Built upon Leaflet.js rendering OpenStreetMap tiles, animating a navigation vehicle puck along the OSM route and triggering proximity warnings hands-free.

---

## 2. AI Usage Declaration Summary

This assignment was developed using **Spec-Driven Phased Vibe-Coding** in collaboration with Google Antigravity Assistant (Gemini 3.8 Flash).

* **AI Role:** Assisting with architectural decomposition, mathematical formulation of Webster's equation and bimodal Gaussian rush-hour congestion, formatting Mermaid diagrams, and generating Web Speech API snippets.
* **Student Role (Human Oversight):**
  - Formulated the Deontic safety rules and defined vehicle ground clearance boundaries ($H_{\text{water}} > H_{\text{safe}} \implies W = +\infty$).
  - Verified Webster's formulation against traffic engineering literature and urban signal timings.
  - Implemented the core algorithms and integrated them with the shared group repository.
  - Performed live git merges with group upstream branches and verified the web demonstration.

Detailed declaration file: [`P01/AI_Declaration.md`](./P01/AI_Declaration.md)

---

## 3. Submission Structure

```text
25125091_06_01/
├── README.md                          # Main lab overview, AI declaration & execution guide
├── git-commit-log.txt                 # Git commit history log
└── P01/                               # Deliverable 01: Individual Feature Submission
    ├── README.md                      # Feature note & group repo dependency instructions
    ├── README.pdf
    ├── report.md                      # Comprehensive academic development report
    ├── report.pdf
    ├── explanation.md                 # Clear feature & API integration explanation
    ├── explanation.pdf
    ├── AI_Declaration.md              # Detailed AI Usage Declaration
    ├── src/                           # Source code of the feature
    │   ├── alerts/
    │   │   ├── __init__.py
    │   │   ├── proximity.py           # Haversine distance & look-ahead route hazard scanner
    │   │   └── voice.py               # Web Speech API prompt & JS script generator
    │   └── signals/
    │       ├── __init__.py
    │       └── webster.py             # Webster 1958 delay models & Binh Thanh 3-intersection lookup
    └── evidence/                      # Video demonstration & visual proof
        └── video.txt                  # Drive link to video demonstrating live web app functionality
        └── git-commit-log-project.txt # Personal commit history log in Group Project
```

---

## 4. Execution & Video Demonstration Guide

### How to Run the Live Web Visualizer (Group 06 Repository)
To experience the full interactive web application with OpenStreetMap map tiles, Apple Maps navigation puck simulation, and browser Web Speech API voice alerts:

> [!NOTE]
> If testing on another machine, please clone the complete Group 06 repository:  
> `git clone https://github.com/Dvhlong55/CS252-Group6.git`  
> (Checkout branch `demo` or `feat/traffic-alert-system`)

```powershell
# 1. Navigate to the Group 06 repository
cd "CS252-Group6"

# 2. Launch the live visualizer server
python server.py 5500

# 3. Open your browser at:
# http://localhost:5500/ (or http://localhost:5500/smartroute_demo.html)
```

**Walkthrough Shown in Video Demonstration:**
1. In the Web UI, select vehicle **Honda Vision (20cm)**.
2. Select route: **Ngã tư Hàng Xanh $\to$ ĐH Ngoại Thương CS2 (Nguyễn Gia Trí)**.
3. Select Scenario: **Đỉnh triều ngập (Flood)** $\implies$ Observe the system automatically reroutes via **Điện Biên Phủ** because Nguyễn Gia Trí is flooded ($30\,\text{cm} > 20\,\text{cm}$).
4. Switch vehicle to **SUV / Everest (50cm)** $\implies$ The system allows passing directly ($30\,\text{cm} \le 50\,\text{cm}$) with caution badges.
5. Click **"Bắt đầu hành trình"** (`btnSimulateDrive`) $\implies$ The navigation puck animates along OpenStreetMap coordinates. When approaching within proximity of the hazard, device vibrates, audio beeps, and browser speaks aloud in Vietnamese.
6. Inspect the ETA card to observe the Webster traffic signal delay decomposition ($\text{ETA} = \text{Driving} + \text{Signals}$).
