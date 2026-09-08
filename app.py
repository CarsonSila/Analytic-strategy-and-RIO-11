"""OpsPulse AI - Enterprise Operations Intelligence & Incident SLA Copilot.
Streamlit Application Entrypoint.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="OpsPulse AI - Operations Intelligence & SLA Copilot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import internal modules
from src.config import config
from src.data_generator import generate_incidents_data, ensure_sample_data_file
from src.analytics import (
    calculate_kpis,
    calculate_mttr_by_severity,
    calculate_service_breakdown,
    detect_operational_anomalies,
    get_at_risk_active_incidents,
)
from src.ai_copilot import ai_copilot
from src.rag_engine import rag_engine
from src.report_generator import generate_executive_daily_report

# Custom CSS for Sleek Modern Enterprise UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #EDF2F7 100%);
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-critical {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .badge-compliant {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 6px 6px 0 0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Session State Initialization
# ------------------------------------------------------------------------------
if "incident_df" not in st.session_state:
    sample_file = ensure_sample_data_file()
    st.session_state.incident_df = pd.read_csv(sample_file)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "👋 Hello! I am your OpsPulse Copilot. Ask me anything about our operational runbooks, incident response procedures, database failover, or API latency troubleshooting."}
    ]

# ------------------------------------------------------------------------------
# Sidebar Controls & Global Filters
# ------------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/server.png", width=64)
    st.title("OpsPulse AI")
    st.caption("⚡ Enterprise Operations & SLA Intelligence")
    st.markdown("---")

    # Data Source Selection
    st.subheader("📁 Data Source")
    data_source_mode = st.radio(
        "Select Source",
        ["Default Dataset", "Generate Fresh Data", "Upload Custom CSV"],
        index=0,
        label_visibility="collapsed"
    )

    if data_source_mode == "Generate Fresh Data":
        num_rows = st.slider("Records to generate", 50, 300, 120, step=25)
        if st.button("🔄 Generate New Dataset", use_container_width=True):
            st.session_state.incident_df = generate_incidents_data(num_records=num_rows, seed=np.random.randint(1, 9999))
            st.success(f"Generated {num_rows} fresh operational records!")

    elif data_source_mode == "Upload Custom CSV":
        uploaded_file = st.file_uploader("Upload CSV incident log", type=["csv"])
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                st.session_state.incident_df = uploaded_df
                st.success("Custom dataset loaded successfully!")
            except Exception as e:
                st.error(f"Error loading CSV: {e}")

    st.markdown("---")
    st.subheader("🔍 Filters")
    df_raw = st.session_state.incident_df.copy()

    # Team Filter
    all_teams = ["All Teams"] + sorted(list(df_raw["team"].dropna().unique())) if "team" in df_raw.columns else ["All Teams"]
    selected_team = st.selectbox("Team / Squad", all_teams)

    # Severity Filter
    all_severities = ["All Severities"] + sorted(list(df_raw["severity"].dropna().unique())) if "severity" in df_raw.columns else ["All Severities"]
    selected_severity = st.selectbox("Severity Level", all_severities)

    # Status Filter
    all_statuses = ["All Statuses"] + sorted(list(df_raw["status"].dropna().unique())) if "status" in df_raw.columns else ["All Statuses"]
    selected_status = st.selectbox("Incident Status", all_statuses)

    # Apply filters
    filtered_df = df_raw.copy()
    if selected_team != "All Teams":
        filtered_df = filtered_df[filtered_df["team"] == selected_team]
    if selected_severity != "All Severities":
        filtered_df = filtered_df[filtered_df["severity"] == selected_severity]
    if selected_status != "All Statuses":
        filtered_df = filtered_df[filtered_df["status"] == selected_status]

    st.markdown("---")
    # SRE Model Configuration Section
    st.subheader("⚙️ SRE Model Config")
    with st.expander("🔧 Isolation Forest Tuning", expanded=False):
        sidebar_contamination = st.slider(
            "Contamination Rate",
            min_value=config.MIN_ANOMALY_CONTAMINATION,
            max_value=config.MAX_ANOMALY_CONTAMINATION,
            value=float(st.session_state.get("contamination_rate", config.current_contamination)),
            step=0.01,
            key="sidebar_contamination_slider",
            help="Proportion of outliers in the operational data expected by the SRE team."
        )
        if sidebar_contamination != config.current_contamination:
            config.set_anomaly_contamination(sidebar_contamination)
            st.session_state.contamination_rate = sidebar_contamination

        st.caption(f"Active Config: `{config.current_contamination:.2f}` (Default: `{config.DEFAULT_ANOMALY_CONTAMINATION}`)")

    st.markdown("---")
    # AI Engine Status
    st.subheader("🤖 AI Engine Status")
    if config.OPENAI_API_KEY:
        st.success(f"🟢 Connected: Live LLM ({config.DEFAULT_AI_MODEL})")
    else:
        st.info("🔵 Mode: Intelligent Heuristic Engine (100% Offline & Secure)")

    st.caption("Version 1.0.0 | Week 10 Ops Tool")

# ------------------------------------------------------------------------------
# Main Application Content
# ------------------------------------------------------------------------------
st.markdown('<div class="main-header">⚡ OpsPulse AI: Operations Intelligence & SLA Copilot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-time incident monitoring, AI root-cause triage, ML anomaly detection, and automated executive reporting.</div>', unsafe_allow_html=True)

tab_dash, tab_triage, tab_anomalies, tab_rag, tab_reports = st.tabs([
    "📊 Executive Dashboard",
    "🤖 AI Incident Triage & Copilot",
    "🔍 ML Anomaly Detection",
    "💬 Ops Runbook Chat (RAG)",
    "📑 Executive Reports"
])

# ------------------------------------------------------------------------------
# TAB 1: EXECUTIVE OPS DASHBOARD
# ------------------------------------------------------------------------------
with tab_dash:
    kpis = calculate_kpis(filtered_df)

    # KPI Metric Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("SLA Compliance", f"{kpis['sla_compliance_rate']}%", delta=f"{kpis['sla_compliance_rate'] - 95.0:.1f}% vs Target" if kpis['sla_compliance_rate'] else None)
    with c2:
        st.metric("Overall MTTR", f"{kpis['overall_mttr_minutes']} min", delta=f"{round(kpis['overall_mttr_minutes'] - 60, 1)}m vs Target", delta_color="inverse")
    with c3:
        st.metric("Total Incidents", f"{kpis['total_incidents']}", f"{kpis['sla_breaches']} Breaches", delta_color="inverse")
    with c4:
        st.metric("In-Flight / Open", f"{kpis['open_incidents']}", f"{kpis['critical_open']} Critical (P1/P2)", delta_color="inverse")
    with c5:
        st.metric("Affected Users", f"{kpis['total_affected_users']:,}", "Blast Radius")

    st.markdown("---")

    # Visualizations Row 1
    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.subheader("📈 Incident Volume & SLA Compliance Trend")
        if not filtered_df.empty and "created_at" in filtered_df.columns:
            plot_df = filtered_df.copy()
            plot_df["date"] = pd.to_datetime(plot_df["created_at"]).dt.date
            trend_df = plot_df.groupby(["date", "sla_status"]).size().reset_index(name="count")
            fig_trend = px.bar(
                trend_df,
                x="date",
                y="count",
                color="sla_status",
                color_discrete_map={"Compliant": "#10B981", "Breached": "#EF4444", "Within SLA": "#3B82F6"},
                barmode="stack",
                title="Daily Incidents by SLA Status"
            )
            fig_trend.update_layout(xaxis_title="Date", yaxis_title="Number of Incidents", legend_title="SLA Status", height=340)
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No data available for trend chart.")

    with col_v2:
        st.subheader("🎯 Severity Distribution")
        if not filtered_df.empty and "severity" in filtered_df.columns:
            sev_counts = filtered_df["severity"].value_counts().reset_index()
            sev_counts.columns = ["severity", "count"]
            fig_sev = px.pie(
                sev_counts,
                names="severity",
                values="count",
                hole=0.45,
                color="severity",
                color_discrete_map={
                    "P1 - Critical": "#DC2626",
                    "P2 - High": "#F97316",
                    "P3 - Medium": "#FBBF24",
                    "P4 - Low": "#34D399"
                },
                title="Incidents by Severity Breakdown"
            )
            fig_sev.update_layout(height=340)
            st.plotly_chart(fig_sev, use_container_width=True)
        else:
            st.info("No data available.")

    # Visualizations Row 2
    col_v3, col_v4 = st.columns(2)

    with col_v3:
        st.subheader("⚙️ Incident Frequency & Breaches by Service")
        svc_df = calculate_service_breakdown(filtered_df)
        if not svc_df.empty:
            fig_svc = px.bar(
                svc_df,
                x="total_incidents",
                y="service",
                orientation="h",
                color="breaches",
                color_continuous_scale=["#3B82F6", "#EF4444"],
                title="Incidents & Breaches Across Microservices"
            )
            fig_svc.update_layout(yaxis={'categoryorder':'total ascending'}, height=340)
            st.plotly_chart(fig_svc, use_container_width=True)
        else:
            st.info("No service breakdown data available.")

    with col_v4:
        st.subheader("⏱️ Average MTTR vs SLA Target by Severity")
        mttr_df = calculate_mttr_by_severity(filtered_df)
        if not mttr_df.empty:
            fig_mttr = go.Figure()
            fig_mttr.add_trace(go.Bar(
                x=mttr_df["severity"],
                y=mttr_df["avg_mttr_min"],
                name="Actual Avg MTTR (min)",
                marker_color="#6366F1"
            ))
            fig_mttr.add_trace(go.Bar(
                x=mttr_df["severity"],
                y=mttr_df["sla_target_min"],
                name="Target SLA (min)",
                marker_color="#94A3B8"
            ))
            fig_mttr.update_layout(barmode="group", yaxis_title="Minutes", height=340)
            st.plotly_chart(fig_mttr, use_container_width=True)
        else:
            st.info("No resolved MTTR data available.")

    # Data Table View
    st.markdown("---")
    st.subheader("📋 Operational Incidents Record Table")
    st.dataframe(
        filtered_df[[
            "incident_id", "title", "service", "severity", "team", "status",
            "sla_status", "duration_minutes", "affected_users", "created_at"
        ]],
        use_container_width=True,
        hide_index=True
    )

    # Export CSV Button
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Incidents to CSV",
        data=csv_data,
        file_name=f"operational_incidents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# ------------------------------------------------------------------------------
# TAB 2: AI INCIDENT TRIAGE & COPILOT
# ------------------------------------------------------------------------------
with tab_triage:
    st.subheader("🤖 AI Incident Triage & Automated Post-Mortem Generator")
    st.markdown("Select an existing incident from the system or enter an un-triaged alert to let the AI classify severity, estimate blast radius, identify root causes, and draft a response runbook.")

    triage_mode = st.radio("Choose Input Mode:", ["Select from Incident Catalog", "Enter Custom Incident / Stack Trace"], horizontal=True)

    if triage_mode == "Select from Incident Catalog":
        incident_options = {
            f"[{row['incident_id']}] {row['title']} ({row['service']})": row
            for _, row in filtered_df.iterrows()
        }
        if incident_options:
            selected_key = st.selectbox("Select Incident to Triage:", list(incident_options.keys()))
            selected_row = incident_options[selected_key]
            
            triage_title = selected_row["title"]
            triage_service = selected_row["service"]
            triage_logs = f"Root Cause hint: {selected_row['root_cause']}\nResolution Notes: {selected_row['resolution_summary']}"
            triage_users = int(selected_row["affected_users"]) if pd.notna(selected_row["affected_users"]) else 100
            current_incident_id = selected_row["incident_id"]
        else:
            st.warning("No incidents available in the current filter.")
            triage_title, triage_service, triage_logs, triage_users, current_incident_id = "", "", "", 0, "INC-CUSTOM"
    else:
        current_incident_id = "INC-LIVE-TRIAGE"
        c_in1, c_in2 = st.columns(2)
        with c_in1:
            triage_title = st.text_input("Incident Title / Alert Summary", value="API Gateway returning 504 Gateway Timeout on checkout")
            triage_service = st.selectbox("Impacted Service", [
                "API Gateway", "Auth & SSO Service", "Payment Gateway", "Primary PostgreSQL DB",
                "Redis Cache Cluster", "Search & Elastic Cluster", "Checkout Pipeline", "Notification & Email Worker"
            ])
        with c_in2:
            triage_users = st.number_input("Estimated Affected Users", min_value=0, max_value=500000, value=1250, step=50)
            triage_logs = st.text_area("Error Trace / Telemetry Logs", value="""ERROR: 2026-08-28 09:12:00 [catalog-service] ConnectionPoolTimeoutException: Timeout waiting for idle connection in pool [size: 50, active: 50, pending: 184]
WARN: 2026-08-28 09:12:05 [api-gateway] Upstream host returned HTTP 504 Gateway Timeout after 5000ms. Shedding traffic.""", height=100)

    if st.button("⚡ Run AI Triage & Root Cause Analysis", type="primary", use_container_width=True):
        with st.spinner("AI analyzing telemetry, error patterns, and runbooks..."):
            triage_res = ai_copilot.triage_incident(
                title=triage_title,
                service=triage_service,
                logs_or_description=triage_logs,
                affected_users=triage_users
            )

        st.success("Triage Analysis Complete!")

        # Display Triage Results
        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric("Recommended Severity", triage_res["recommended_severity"])
        with r2:
            st.metric("Target SLA Budget", f"{triage_res['sla_target_minutes']} min")
        with r3:
            st.metric("Estimated Blast Radius", f"{triage_res['blast_radius_score']}/100")

        st.markdown(f"**AI Engine Mode:** `{triage_res.get('mode', 'OpsPulse Copilot')}`")

        c_box1, c_box2 = st.columns(2)
        with c_box1:
            st.markdown("### 🔍 Root Cause Hypothesis")
            st.info(triage_res["root_cause_hypothesis"])

            st.markdown("### 📖 Matched Operational Runbook")
            st.code(f"data/runbooks/{triage_res['matching_runbook']}", language="bash")

        with c_box2:
            st.markdown("### 🛠️ Recommended Remediation Checklist")
            for idx, step in enumerate(triage_res["remediation_checklist"], 1):
                st.markdown(f"{idx}. {step}")

        # Post-Mortem Generator Section
        st.markdown("---")
        st.subheader("📝 Executive Incident Post-Mortem Generator")
        if st.button("📄 Generate Executive Post-Mortem Report", use_container_width=True):
            post_mortem_md = ai_copilot.generate_post_mortem(
                incident_id=current_incident_id,
                title=triage_title,
                service=triage_service,
                severity=triage_res["recommended_severity"],
                root_cause=triage_res["root_cause_hypothesis"],
                duration_minutes=int(triage_res["sla_target_minutes"] * 0.75),
                affected_users=triage_users
            )
            st.markdown("#### Post-Mortem Preview")
            st.markdown(post_mortem_md)
            st.download_button(
                label="📥 Download Post-Mortem (.md)",
                data=post_mortem_md,
                file_name=f"post_mortem_{current_incident_id}.md",
                mime="text/markdown"
            )

# ------------------------------------------------------------------------------
# TAB 3: ML ANOMALY DETECTION & SLA RISK
# ------------------------------------------------------------------------------
with tab_anomalies:
    st.subheader("🔍 ML Operational Anomaly Detection & At-Risk SLA Predictor")
    st.markdown("Using **Isolation Forest** unsupervised machine learning and statistical models to flag anomalous high-duration incidents, user impact spikes, and in-flight SLA breach risks.")

    col_anom1, col_anom2 = st.columns([1, 1])

    with col_anom1:
        st.markdown("#### ⚙️ SRE Model Parameter Configuration")
        tab_contamination = st.slider(
            "Isolation Forest Contamination Rate (Expected Anomaly %)",
            min_value=config.MIN_ANOMALY_CONTAMINATION,
            max_value=config.MAX_ANOMALY_CONTAMINATION,
            value=float(config.current_contamination),
            step=0.01,
            key="tab_contamination_slider",
            help="SRE configuration setting defining the proportion of operational anomalies expected by the Isolation Forest model."
        )
        if tab_contamination != config.current_contamination:
            config.set_anomaly_contamination(tab_contamination)
            st.session_state.contamination_rate = tab_contamination

        st.caption(f"🔧 Config Setting: `config.current_contamination = {config.current_contamination:.2f}` (System Default: `{config.DEFAULT_ANOMALY_CONTAMINATION}`)")

        anomaly_df = detect_operational_anomalies(filtered_df, contamination=config.current_contamination)
        anomalies_detected = anomaly_df[anomaly_df["is_anomaly"]]

        st.metric("Total Anomalies Detected", f"{len(anomalies_detected)}", f"{round(len(anomalies_detected)/len(anomaly_df)*100, 1)}% of total" if len(anomaly_df) else "0%")

    with col_anom2:
        if not anomaly_df.empty:
            fig_scatter = px.scatter(
                anomaly_df,
                x="duration_minutes",
                y="affected_users",
                color="is_anomaly",
                color_discrete_map={True: "#EF4444", False: "#3B82F6"},
                hover_data=["incident_id", "title", "service", "anomaly_reason"],
                title="ML Anomaly Boundary: Duration vs Affected Users"
            )
            fig_scatter.update_layout(height=320)
            st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("### 🚨 Detected Anomalies Log")
    if not anomalies_detected.empty:
        st.dataframe(
            anomalies_detected[[
                "incident_id", "title", "service", "severity", "duration_minutes",
                "affected_users", "anomaly_reason", "anomaly_score"
            ]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("✅ No operational anomalies detected in the selected filter window.")

    st.markdown("---")
    st.subheader("⏱️ Live At-Risk In-Flight Incidents (SLA Breach Predictor)")
    at_risk_df = get_at_risk_active_incidents(filtered_df)
    if not at_risk_df.empty:
        st.warning(f"⚠️ {len(at_risk_df)} active incident(s) currently consuming SLA budget.")
        st.dataframe(
            at_risk_df[[
                "incident_id", "title", "service", "severity", "elapsed_minutes",
                "sla_target_minutes", "sla_budget_used_pct", "risk_level"
            ]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("✅ Zero active in-flight incidents currently exceeding or approaching SLA thresholds.")

# ------------------------------------------------------------------------------
# TAB 4: OPS RUNBOOK CHATBOT (RAG)
# ------------------------------------------------------------------------------
with tab_rag:
    st.subheader("💬 Ops Runbook Knowledge Assistant (RAG Chat)")
    st.markdown("Ask natural language questions about infrastructure troubleshooting, failovers, and incident response procedures. Powered by grounded operational runbooks.")

    # Quick prompt shortcuts
    st.markdown("**Quick Prompts:**")
    qp1, qp2, qp3 = st.columns(3)
    quick_query = None
    with qp1:
        if st.button("🐘 How to triage PostgreSQL replication lag?"):
            quick_query = "How to triage PostgreSQL replication lag and failover?"
    with qp2:
        if st.button("⚡ What to do on API Gateway 504 timeouts?"):
            quick_query = "What to do when API Gateway returns 504 timeouts?"
    with qp3:
        if st.button("💳 How to recover Stripe webhook failures?"):
            quick_query = "How to recover Stripe webhook rate limit failures?"

    # Display Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    user_input = st.chat_input("Ask a question about operational runbooks...") or quick_query
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Searching runbook knowledge base..."):
                response = rag_engine.answer_query(user_input)
                st.markdown(response["answer"])
                if response.get("sources"):
                    st.caption(f"📚 **Grounded Runbook Sources:** {', '.join(response['sources'])}")

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"{response['answer']}\n\n*Sources: {', '.join(response.get('sources', []))}*"
        })

# ------------------------------------------------------------------------------
# TAB 5: AUTOMATED DAILY EXECUTIVE BRIEFING
# ------------------------------------------------------------------------------
with tab_reports:
    st.subheader("📑 Automated Daily Executive Briefing & Report Generator")
    st.markdown("Generate an automated, C-level executive summary of daily operations, SLA compliance, MTTR performance, and recommended next steps.")

    col_rep_date, col_rep_btn = st.columns([2, 1])
    with col_rep_date:
        report_date_selected = st.date_input("Report Date", value=datetime.today())
    with col_rep_btn:
        st.write("")
        st.write("")
        gen_clicked = st.button("🚀 Generate Executive Briefing", type="primary", use_container_width=True)

    report_text = generate_executive_daily_report(filtered_df, report_date=str(report_date_selected))

    st.markdown("### 📄 Executive Briefing Preview")
    st.markdown(report_text)

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📥 Download Executive Briefing (.md)",
            data=report_text,
            file_name=f"executive_ops_briefing_{report_date_selected}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col_dl2:
        kpis_df = pd.DataFrame([calculate_kpis(filtered_df)])
        st.download_button(
            label="📥 Download Daily KPI Metrics (.csv)",
            data=kpis_df.to_csv(index=False).encode('utf-8'),
            file_name=f"kpi_metrics_{report_date_selected}.csv",
            mime="text/csv",
            use_container_width=True
        )

