"""Unit tests for RAG engine and executive report generator."""
from src.rag_engine import rag_engine
from src.report_generator import generate_executive_daily_report
from src.data_generator import generate_incidents_data

def test_rag_engine_retrieve():
    docs = rag_engine.retrieve_relevant_docs("database failover postgresql", top_k=1)
    assert len(docs) > 0
    assert "database_failover" in docs[0]["filename"]

def test_rag_engine_answer():
    ans = rag_engine.answer_query("How do I failover a postgres database?")
    assert "answer" in ans
    assert len(ans["sources"]) > 0

def test_generate_executive_daily_report():
    df = generate_incidents_data(num_records=40, seed=99)
    report = generate_executive_daily_report(df, report_date="2026-08-28")
    assert "Daily Executive Operations Briefing" in report
    assert "Global SLA Compliance" in report
    assert "2026-08-28" in report

