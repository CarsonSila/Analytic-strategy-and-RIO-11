"""Unit tests for synthetic incident data generator."""
import pandas as pd
from src.data_generator import generate_incidents_data, ensure_sample_data_file

def test_generate_incidents_data_shape():
    df = generate_incidents_data(num_records=25, seed=42)
    assert len(df) == 25
    expected_cols = [
        "incident_id", "title", "service", "severity", "team",
        "status", "assigned_engineer", "created_at", "sla_target_minutes",
        "sla_status", "affected_users", "root_cause", "resolution_summary"
    ]
    for col in expected_cols:
        assert col in df.columns

def test_ensure_sample_data_file():
    path = ensure_sample_data_file()
    assert path.exists()
    df = pd.read_csv(path)
    assert not df.empty

