# 🏆 Hackathon #3 Official Submission Package
**Project Title:** OpsPulse AI — Enterprise Operations Intelligence & SLA Copilot  
**Team Name:** OpsPulse SRE & Analytics Innovations  
**Lead Developer / Presenter:** Carson Sila Wambua (B.Sc IT, Zetech University & Inuka Fellow)  
**Target Repository:** [https://github.com/CarsonSila/Analytic-strategy-and-RIO-11](https://github.com/CarsonSila/Analytic-strategy-and-RIO-11)  
**Evaluation Standard:** Hackathon #3 In-Person & Final Board Presentation  

---

## 🚀 1. Executive Summary & Pitch Overview
In 24/7 Network Operations Centers (NOC) and cloud environments, alert fatigue and manual incident triage cost organizations hundreds of thousands of dollars in contractual SLA penalties and wasted engineering labor. 

**OpsPulse AI** is an operational intelligence and site reliability copilot that ingests streaming incident telemetry, detects multivariate operational anomalies before service degradation occurs, generates 1-click 5-Whys root cause post-mortems, and prescribes production-grade CLI remediation commands using grounded SRE runbooks.

---

## 📊 2. Strategic Business Case & Financial Impact
- **Initial Capital Investment (CAPEX):** $45,000 (Development, ML calibration, enterprise integration)
- **Annual Operating Costs (OPEX):** $12,000 / year (Cloud hosting, automated alerting)
- **Total Year 1 Cost:** $57,000
- **Gross Annual Savings:** **$320,000 / year**
  - Contractual SLA Breach Penalty Elimination (-65%): **$208,000**
  - SRE / NOC Engineering Time Recovered (990 hours @ $50/hr): **$49,500**
  - Customer SLA Retention & Churn Mitigation: **$62,500**
- **Net Year 1 Benefit:** $320,000 - $57,000 = **$263,000**
- **Year 1 Net ROI:** **461.4%**
- **Payback Period:** **1.75 Months (53 Calendar Days)**
- **Mean Time to Resolution (MTTR):** Slashed by **73%** (from 45 minutes down to 12 minutes)

*For the complete CFO/Board document, refer to [`Week11_Business_Case_CarsonWambua.pdf`](Week11_Business_Case_CarsonWambua.pdf).*

---

## 🛠️ 3. Working Code Architecture & Technical Stack

```
├── app.py                      # Main Streamlit Multi-Tab Operations Intelligence Dashboard
├── requirements.txt            # Python dependencies (Streamlit, Scikit-Learn, Plotly, etc.)
├── src/
│   ├── __init__.py
│   ├── config.py              # Centralized configuration & SLA constants
│   ├── data_generator.py      # Enterprise synthetic incident generator (1,800+ records)
│   ├── analytics.py           # SRE KPIs, MTTR logic, Isolation Forest Anomaly Detection
│   ├── ai_copilot.py          # AI Incident Triage Engine (Dual-mode offline/online)
│   ├── rag_engine.py          # Grounded operational runbook RAG search
│   └── report_generator.py    # Automated executive daily briefing compiler
├── data/
│   ├── sample_incidents.csv   # Pre-populated enterprise operational dataset
│   └── runbooks/              # SRE markdown knowledge base
│       ├── database_failover.md
│       ├── api_gateway_latency.md
│       ├── auth_service_outage.md
│       └── payment_gateway_timeout.md
└── tests/
    ├── __init__.py
    ├── test_analytics.py      # Unit tests for KPI calculations and ML anomaly bounds
    ├── test_data_generator.py # Tests for synthetic data generation schemas
    ├── test_ai_copilot.py     # Tests for offline fallback and triage output formats
    └── test_rag_and_reports.py# Tests for RAG search accuracy and report exports
```

### Core Technologies:
- **Frontend / Dashboard:** Streamlit 1.35+, Plotly Interactive Charts
- **Analytics & Machine Learning:** Scikit-Learn (`IsolationForest`), Pandas, NumPy, SciPy
- **Operational Logic:** Dual-mode heuristic fallback with grounded RAG knowledge search
- **Testing & Validation:** Pytest (13 automated tests), Great Expectations data schemas

---

## 🏃 4. Quickstart & Execution Instructions

```bash
# 1. Clone repository
git clone https://github.com/CarsonSila/Analytic-strategy-and-RIO-11.git
cd Analytic-strategy-and-RIO-11

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run automated test suite
python -m pytest tests/

# 4. Launch the interactive operational dashboard
streamlit run app.py
```

---

## 🎥 5. Performance & Presentation Deliverables
- **15-Minute Strategy Pitch Deck:** [`Week11_Pitch_Deck.pdf`](Week11_Pitch_Deck.pdf) (12 landscape 16:9 slides designed for Board & CFO review).
- **Mock Interview Highlights Reel:** [`Week11_Mock_Interview.mp4`](Week11_Mock_Interview.mp4) (HD 720p executive presentation of core STAR Q&As).
- **Interview Transcript & STAR Guide:** [`MOCK_INTERVIEW_TRANSCRIPT_AND_STAR_GUIDE.md`](MOCK_INTERVIEW_TRANSCRIPT_AND_STAR_GUIDE.md).
- **Executive Self-Reflection:** [`Week11_Self_Reflection.md`](Week11_Self_Reflection.md) (~200 words reflecting on delivery, strengths, and areas for growth).

---

## 👥 6. Team Contribution Breakdown
- **Carson Sila Wambua (Lead Developer & Strategy):**  
  Architected the end-to-end data ingestion pipeline, built the Scikit-Learn `IsolationForest` anomaly engine, developed the dual-mode offline heuristic fallback copilot, authored the financial business case model and 1-page CFO brief, and delivered the board pitch presentation.
