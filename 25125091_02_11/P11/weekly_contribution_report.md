# Week 2 Contribution Report

**Name:** Tran Duc Toan  
**Student ID:** 25125091  
**Group:** 6  
**Project:** SmartRoute (CS252 - Computational Thinking)  
**Week:** 4

## Git Commit Log Note
Please note that I do not have a Git commit log to attach for this week. My assigned tasks for this phase of the project were strictly focused on theoretical research, mathematical abstraction, technical writing for the project report, and slide design. No codebase modifications were required or made by me during this reporting period. Below is the detailed summary of my direct contributions to the team's deliverables.

## Summary of Contributions This Week

This week, my primary responsibility was researching and formulating **Section 3.a: Traffic Signal Delay Modeling**, applying the 4 pillars of Computational Thinking, and preparing the corresponding presentation materials.

### 1. Report Section 3.a (Traffic Signal Delay Modeling)
I researched, structured, and wrote the complete technical documentation for our traffic signal delay solution, strictly following the TA's required "3-beat debate" format.

* **The Split (Decomposition):** I formulated two competing technical approaches to address the "velocity smoothing" blind spot in commercial routing apps: 
  * *Track A:* Deterministic SPaT (Signal Phase and Timing) tracking.
  * *Track B:* Stochastic expected delay modeling based on queuing theory.
* **The Debate & Trade-offs:** I analyzed the pros and cons of both models. Crucially, I contextualized this for Ho Chi Minh City by highlighting that Track A (Deterministic) completely fails when traffic police manually override signals during peak hours, whereas Track B remains robust.
* **Tentative Selection & Abstraction:** I formalized our decision to use a Hybrid Stochastic model. I developed and documented the mathematical abstraction formula used to convert red-light probabilities and congestion factors into an Equivalent Time Cost ($W_{eff}$) that our routing graph can directly ingest: $E[Delay] = \frac{R^2}{2(R+G)} \times C(t)$.

### 2. Presentation Design (Canva)
I translated my technical report section into a highly visual, 6-slide presentation deck using Canva, adhering to the APCS presentation standards. 

* **Visual Storytelling:** Designed the "Micro Blind Spot" introduction to visually contrast continuous fluid flow (Google Maps) with discrete junction delays.
* **Information Architecture:** Created a clear side-by-side comparison layout for "The Split" and built a concise Trade-offs matrix table focusing on Accuracy vs. Real-world Resilience.
* **Mathematical Typography:** Formatted the core abstraction formula clearly on a dedicated slide to highlight our application of Computational Thinking.
* **Contextual Walkthrough:** Designed a concrete scenario (Dien Bien Phu corridor) to demonstrate how our mathematical model corrects a 4-minute Google Maps ETA to a highly accurate 6.7-minute real-world ETA. 