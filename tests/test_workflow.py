from pathlib import Path

from afyaflow.workflow import run_report_workflow

ROOT = Path(__file__).resolve().parents[1]


def test_run_report_workflow_returns_alert_handoff_and_audit(tmp_path: Path) -> None:
    audit_path = tmp_path / "audit.jsonl"
    result = run_report_workflow(
        "Old Town Health Centre tuko na ORS sachets 12 tu, matumizi ni 6 kwa siku.",
        inventory_path=ROOT / "data" / "synthetic" / "facility_inventory.json",
        audit_path=audit_path,
        handoff_language="sw",
    )

    assert result["report"].facility == "Old Town Health Centre"
    assert result["risk"].level == "red"
    assert result["risk"].transfer_rank
    assert "Tahadhari" in result["handoff"]
    assert audit_path.exists()
    assert "workflow_completed" in audit_path.read_text(encoding="utf-8")
