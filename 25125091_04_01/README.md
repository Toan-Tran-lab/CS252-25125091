# Lab 04: From Spec to Code - Phased Vibe-coding with AI

> **Course:** CS252 – Computational Thinking, Class 25A01  
> **Student:** Tran Duc Toan (Trần Đức Toàn)  
> **Student ID:** 25125091  
> **Group Project:** SmartRoute (Group 06)  

---

## 1. AI Usage Declaration

This assignment was developed using **Spec-Driven Phased Vibe-Coding** in collaboration with Google Antigravity Assistant (Gemini 3.8 Flash).

* **AI Role:** Assisting with architectural decomposition, mathematical modeling (Webster 1958 delay formulation), generating comprehensive unit test suites, and formatting Mermaid design artifacts.
* **Student Role (Human Oversight):** 
  - Defined system boundaries, Interface Contracts, and Deontic safety constraints ($H_{\text{water}} > H_{\text{safe}} \implies \text{CRITICAL}$).
  - Strictly reviewed mathematical validity, audited boundary edge-case handling, and directed commit scope granularity.
  - Executed and validated all 20 unit tests and live simulations locally.

Detailed declaration file: [`P01/AI_Declaration.md`](./P01/AI_Declaration.md)

---

## 2. Submission Structure

```text
25125091_04_01/
├── README.md                      # AI Usage Declaration, structure & reproduction guide
├── git-commit-log.txt             # Exported Git commit history
└── P01/                           # Deliverable 01: Vibe-coding one course project feature
    ├── report.md                  # Comprehensive development report with Mermaid artifacts & evidence
    ├── report.pdf                 # PDF version of the development report
    ├── AI_Declaration.md          # Detailed AI declaration
    ├── demo_feature_in_action.py  # Standalone visual simulation script
    ├── git-commit-log.txt         # Commit log backup
    ├── evidence/                  # Screenshots of feature execution and unit tests
    │   ├── evidence (1).png       # Demo: Road closures, defects & lookahead scan
    │   ├── evidence (2).png       # Unit Tests: 20/20 test suite execution
    │   ├── evidence (3).png       # Demo: Webster signal delay across time-of-day
    │   └── evidence (4).png       # Demo: Deontic flood warnings across vehicle classes
    ├── src/                       # Feature source code (signals & alerts)
    │   ├── signals/               # Module M3: Webster delay calculation
    │   └── alerts/                # Proximity hazard alert triggers
    └── tests/                     # Automated unit test suite (20 tests)
        ├── test_webster_signal.py
        └── test_traffic_alert.py
```

Detailed feature development report: [`P01/report.md`](./P01/report.md)

---

## 3. How to Reproduce & Execution Guide

To reproduce all unit tests and visual feature demonstrations on any generic machine (Windows, macOS, or Linux), follow the instructions below. These steps use portable relative paths without any machine-specific hardcoded directories.

### System Requirements & Dependencies
* **Python:** Version 3.10 or higher.
* **Core Libraries:** Standard library only (`unittest`, `math`, `dataclasses`, `enum`, `typing`).
* **Optional Graph Package (for full team router integration):**
  ```bash
  pip install networkx pyyaml
  ```

---

### Option A: Running within the Group Repository (`CS252-Group6`)
This is the recommended workflow when inspecting the complete codebase on branch `feat/traffic-alert-system`:

```bash
# 1. Clone the team repository and checkout the feature branch
git clone https://github.com/Dvhlong55/CS252-Group6.git
cd CS252-Group6
git checkout feat/traffic-alert-system

# 2. Configure the Python module search path (PYTHONPATH)
# On Windows PowerShell:
$env:PYTHONPATH="src"
# On Linux / macOS / Git Bash:
export PYTHONPATH="src"

# 3. Execute all 20 automated unit tests
python -m unittest -v tests/routing/test_webster_signal.py tests/routing/test_traffic_alert.py
# (Expected result: Ran 20 tests - OK)

# 4. Execute the interactive live feature demonstration
python demo_feature_in_action.py
```

---

### Option B: Running from the Personal Lab Submission Folder (`25125091_04_01/P01`)
When evaluating this standalone deliverable directory alongside the cloned team repository:

```text
workspace/
├── CS252-25125091/          # Personal Lab Repository
│   └── 25125091_04_01/P01/  # Feature deliverable folder
└── CS252-Group6/            # Cloned Group 06 Repository
```

```bash
# 1. Navigate to the deliverable folder
cd CS252-25125091/25125091_04_01/P01

# 2. Configure PYTHONPATH using portable relative paths
# On Windows PowerShell:
$env:PYTHONPATH="src;../../../CS252-Group6/src"
# On Linux / macOS / Git Bash:
export PYTHONPATH="src:../../../CS252-Group6/src"

# 3. Execute all 20 automated unit tests
python -m unittest -v tests/test_webster_signal.py tests/test_traffic_alert.py

# 4. Execute the interactive live feature demonstration
python demo_feature_in_action.py
```
