# AI Usage Declaration

> **Course:** CS252 – Computational Thinking  
> **Assignment:** Lab 04 – From Spec to Code: Phased Vibe-coding with AI  
> **Student Name:** Tran Duc Toan (Trần Đức Toàn)  
> **Student ID:** 25125091 | **Class:** 25A01  

---

## 1. AI Tooling & Environment
* **Primary AI Engine:** Google Antigravity Assistant (powered by Gemini 3.8 Flash).
* **Work Environment:** Interactive pair-programming directly within the local workspace environment.

---

## 2. Phased Scope of AI Collaboration (Spec-Driven Workflow)

The collaboration with the AI assistant followed structured, phased software engineering methodologies:

1. **Reconnaissance & Requirement Analysis:**
   * Assisted in surveying project documentation, course specifications, and analyzing upstream repository contracts (such as Thái Bảo's `feat/osm-routing` graph representations and protocol interfaces).
2. **Interface Contract & Architecture Design:**
   * Formulated and reviewed formal API function signatures: `signal_delay(red_s, green_s, congestion_factor)` and `AlertPayload` dataclass schemas to ensure seamless cross-module interoperability.
3. **Phased Code Generation & Automated Test Suites:**
   * Synthesized Module M3 Webster traffic delay logic (`src/signals/webster.py`) across 3 Computational Thinking iterations.
   * Implemented the real-time proximity alert scanner (`src/alerts/proximity.py`) enforcing Deontic vehicle safety tiers.
   * Generated an automated test suite comprising 20 unit tests with defensive edge-case coverage.
4. **Design Artifacts as Code:**
   * Formatted and rendered Mermaid architectural diagrams: Sequence Diagram for route proximity alerts and State Machine Diagram for Deontic safety state lifecycles.

---

## 3. Human Oversight & Engineering Verification

* **Mathematical Verification:** The student independently verified Webster’s formulation against the seminal paper (Webster, 1958) to ensure the probabilistic arrival formula $E[\text{wait}] = \frac{R^2}{2(R+G)}$ and saturation degree logic were correctly implemented.
* **Deontic Constraint Enforcement:** The student strictly audited the Deontic rule boundaries, guaranteeing that water depths exceeding vehicle ground clearance ($H_{\text{water}} > H_{\text{safe}}$) strictly trigger non-negotiable `CRITICAL` alerts and failover rerouting rather than finite penalties.
* **Granular Commit Control & Acceptance:** The student directed commit message style and scope, executed all 20 automated tests locally, diagnosed runtime dictionary-lookup edge cases, and reviewed all diffs before merging.
