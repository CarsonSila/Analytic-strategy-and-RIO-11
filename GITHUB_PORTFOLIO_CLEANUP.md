# 🐙 GitHub Portfolio & Repository Cleanup Strategy
**Candidate:** Carson Sila Wambua  
**GitHub Profile:** [https://github.com/CarsonSila](https://github.com/CarsonSila)  
**Primary Flagship Repository:** `distributor_financing_backend` (E&M Technology House)  
**Target Submission Repository:** [https://github.com/CarsonSila/Analytic-strategy-and-RIO-11](https://github.com/CarsonSila/Analytic-strategy-and-RIO-11)  

---

## 1. GitHub Profile README Template (`CarsonSila/CarsonSila/README.md`)

```markdown
# Hi there, I'm Carson Sila Wambua 👋
### Backend Software Developer (E&M Technology House) & Operational Data Analyst

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/carson-wambua-5b54442b6)
[![Email](https://img.shields.io/badge/Email-Contact_Me-EA4335?style=flat&logo=gmail)](mailto:wambuacarson@gmail.com)
[![CV](https://img.shields.io/badge/CV-Download_PDF-1E3A8A?style=flat&logo=adobeacrobatreader)](https://github.com/CarsonSila/Analytic-strategy-and-RIO-11/blob/main/CV_CarsonWambua_DataAnalyst.pdf)

---

### 🔭 About Me
- 💼 **Backend Developer at E&M Technology House**: Building high-throughput enterprise microservices for our flagship **Distributor Financing & Anchor Supply Chain Platform** using **Java 21, Spring Boot 3.4, and Spring Cloud**.
- 💳 Core engineer behind the **Onboarding** (multi-tenant KYC & RBAC) and **Repayments** microservices (M-Pesa/CBS payment rails, waterfall allocation, maker-checker governance).
- 🚀 **Operational Data Analyst & SRE**: Creator of **OpsPulse AI**, cutting incident triage time by 73% and eliminating $320K in annualized SLA penalties.
- 📡 Telecom infrastructure engineering foundation at **Quavatel Limited** supporting Safaricom, Airtel, and Liquid Telecom (99.8% SLA uptime).
- 🎓 Completing B.Sc in Information Technology at **Zetech University** (Expected graduation: Nov 2026).

---

### 🛠️ Core Tech Stack & Tools
- **Backend & Microservices:** Java 21, Spring Boot 3.4, Spring Cloud (Eureka Discovery, API Gateway, Config Server), Feign, REST APIs, OpenAPI/Swagger, Maven, Docker, Jenkins
- **Fintech & Payment Rails:** Multi-Tenant Onboarding, KYC Document Processing, M-Pesa C2B/B2B APIs, Core Banking System (CBS) Callbacks, Waterfall Debt Repayment Engine
- **Data Analytics & ML:** Python (Pandas, NumPy, Scikit-Learn, SciPy), SQL (MySQL, PostgreSQL), Isolation Forest Anomaly Detection, Streamlit, Plotly
- **Operations & Systems:** 24/7 NOC Monitoring, SLA/MTTR Optimization, Fiber Splicing & OTDR Diagnostics, Git/GitHub, Linux

---

### 🌟 Featured Top 3 Strategic Projects

| Project | Core Stack | Key Impact |
| :--- | :--- | :--- |
| **[Distributor Financing Platform (Top Project ⭐)](https://github.com/CarsonSila/distributor_financing_backend)** | Java 21, Spring Boot 3.4, Spring Cloud, MySQL, M-Pesa | Enterprise closed-loop supply chain financing; built **Onboarding & Repayments** microservices |
| **[OpsPulse AI: Operations Intelligence & SLA Copilot](https://github.com/CarsonSila/Analytic-strategy-and-RIO-11)** | Python, Streamlit, Scikit-Learn, Plotly | **-73% MTTR**, $320K annual SLA cost avoidance, 15 passed pytest tests |
| **[Predictive Equipment Vibration ML Classifier](https://github.com/CarsonSila/operational-vibration-predictive-ml)** | Python, Scikit-Learn, Pandas, FFT | **0.94 ROC-AUC**, 48h advance mechanical failure prediction |
```

---

## 2. Project 1 README (Flagship ⭐): Distributor Financing Backend Platform

```markdown
# 🏦 Distributor Financing & Supply Chain Fintech Platform (Backend)
**Organization:** E&M Technology House  
**Core Developer:** Carson Sila Wambua (Onboarding & Repayments Microservices)  

[![Java](https://img.shields.io/badge/Java-21-orange.svg)](https://www.oracle.com/java/)
[![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.4.4-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Spring Cloud](https://img.shields.io/badge/Spring_Cloud-2024.0.1-green.svg)](https://spring.io/projects/spring-cloud)
[![Database](https://img.shields.io/badge/MySQL-8.0-blue.svg)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)](https://www.docker.com/)

An enterprise microservices-based financial technology backend powering a closed-loop **Distributor Financing & Anchor Supply Chain Finance Ecosystem**. The platform connects partner commercial banks, anchor manufacturers, and FMCG distributors to finance inventory purchase orders with zero cash diversion risk.

---

### 🏗️ Microservices Architecture & Ecosystem

```
┌─────────────────────────────────────────────────────────────────┐
│               Spring Cloud API Gateway (Port 8080)              │
│                 (Aggregated Swagger / OpenAPI UI)               │
└───────────────┬─────────────────────────────────┬───────────────┘
                │                                 │
   ┌────────────┴────────────┐       ┌────────────┴────────────┐
   │ Eureka Discovery (8761) │       │   Config Server (8888)  │
   └────────────┬────────────┘       └────────────┬────────────┘
                │                                 │
 ┌──────────────┼────────────────┬────────────────┼──────────────┐
 │              │                │                │              │
▼              ▼                ▼                ▼              ▼
Authentication Onboarding       Loans            Repayments     Reports / Notif
(Port 8081)    (Port 8082) ⭐    (Port 8083)      (Port 8084) ⭐  (8085 / 8086)
```

---

### 🎯 Key Contributions by Carson Sila Wambua

#### 1. 📋 Onboarding Microservice (Port 8082)
- **Multi-Tenant Hierarchy:** Built scalable onboarding architectures supporting three distinct legal entities: **Partner Banks, Anchor Manufacturers, and FMCG Distributors**.
- **Automated KYC & Document Processing:** Engineered secure document ingestion (`DistributorDocumentController`, `DocumentStorageService`) for audited tax certificates, trading licenses, and bank statements.
- **Granular RBAC & Tenant Permissions:** Designed role management and privilege evaluation ensuring complete multi-tenant data isolation.
- **Inter-Service Orchestration:** Integrated Feign clients for seamless communication with Authentication, Loans, and Notification services.

#### 2. 💳 Repayments Microservice (Port 8084)
- **High-Reliability Payment Callbacks:** Engineered webhook listeners for **M-Pesa (C2B / B2B)** and **Core Banking System (CBS)** debit responses, ensuring idempotency and strict ACID compliance.
- **Dynamic Waterfall Allocation Engine:** Implemented `FeesInterestPrincipalStrategy` to automatically allocate incoming repayments in priority order:
  $$\text{Incoming Repayment} \longrightarrow \text{Penalties} \longrightarrow \text{Accrued Fees} \longrightarrow \text{Interest} \longrightarrow \text{Principal Reduction}$$
- **Revolving Credit Headroom Recycling:** As principal is retired, the system automatically triggers Feign calls to the Loans service to immediately restore available borrowing capacity.
- **Maker-Checker Financial Governance:** Implemented dual-control verification workflows (`BankMakerVerifyRequest` / `BankCheckerApproveUpdateRequest`) for manual adjustments, waivers, and reversals.
- **Batch Sweep Execution & Ledger Reconciliation:** Built scheduled batch sweeps (`BatchSweepExecutionService`, `RepaymentScheduler`) and automated reconciliation discrepancy audits (`ReconciliationService`).

#### 3. 🤝 Cross-Microservice Collaboration
- Actively collaborating on the **Loans Microservice** (credit risk scoring, facility management, 2-phase disbursement workflows) and **API Gateway / Config Server** setup.

---

### 🚀 Running the Platform Locally

```bash
# 1. Start Config Server & Eureka Discovery
cd config-server && mvn spring-boot:run
cd discovery && mvn spring-boot:run

# 2. Start API Gateway
cd api-gateway && mvn spring-boot:run

# 3. Launch Core Business Microservices
cd onboarding && mvn spring-boot:run
cd repayments && mvn spring-boot:run
cd loans && mvn spring-boot:run
```
```

---

## 3. Project 2 README: OpsPulse AI (Operations Intelligence & SLA Copilot)

*(Full OpsPulse AI documentation including SRE KPIs, Isolation Forest anomaly models, 5-Whys triage, and 15 passed unit tests as documented in the repository).*

---

## 4. Project 3 README: Predictive Equipment Vibration ML Classifier

*(Full Machine Learning explainer and predictive failure classifier on sensor telemetry achieving 0.94 ROC-AUC).*
