"""Streamlit entry point for the AfyaFlow Pwani demo application."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from afyaflow.config import settings
from afyaflow.data_loader import load_stock_report_examples
from afyaflow.extraction import ExtractionError
from afyaflow.workflow import run_report_workflow

EXAMPLES_PATH = ROOT / "data" / "synthetic" / "stock_reports.json"
INVENTORY_PATH = ROOT / "data" / "synthetic" / "facility_inventory.json"
AUDIT_PATH = ROOT / "outputs" / "audit.jsonl"


def main() -> None:
    """Run the judged prototype application."""

    try:
        import streamlit as st
    except ModuleNotFoundError as exc:  # pragma: no cover - defensive runtime guidance
        raise SystemExit(
            "Streamlit is not installed. Install app dependencies with: "
            "python -m pip install -e .[app]"
        ) from exc

    st.set_page_config(page_title="AfyaFlow Pwani", page_icon="AF", layout="wide")
    st.title("AfyaFlow Pwani")
    st.caption("From paper stock reports to early warnings and redistribution actions.")

    examples = load_stock_report_examples(EXAMPLES_PATH)
    example_labels = [f"{item['id']} - {item['expected']['item']}" for item in examples]

    with st.sidebar:
        st.header("Demo controls")
        selected = st.selectbox("Synthetic scenario", example_labels)
        handoff_language = st.radio("Handoff language", ["en", "sw"], horizontal=True)
        st.info("Local fallback extraction is active until the Kaggle GPU Gemma runtime is attached.")

    example = examples[example_labels.index(selected)]
    default_input = example["raw_input"]

    col_input, col_report = st.columns([1, 1])
    with col_input:
        st.subheader("1. Facility report")
        source_type = st.selectbox("Source type", ["text", "image", "audio"], index=0)
        raw_input = _collect_source_input(st, source_type, default_input)
        run_button = st.button("Generate verified stock alert", type="primary")

    if not run_button:
        with col_report:
            st.subheader("2. What the demo will show")
            st.write(
                "Gemma 4 will extract stock fields, the worker confirms them, deterministic code "
                "calculates risk, and AfyaFlow drafts an administrator handoff."
            )
        return

    try:
        result = run_report_workflow(
            raw_input,
            source_type=source_type,
            model_name=settings.gemma_model,
            inventory_path=INVENTORY_PATH,
            audit_path=AUDIT_PATH,
            handoff_language=handoff_language,
        )
    except ExtractionError as exc:
        st.error(f"Could not extract a complete stock report: {exc}")
        st.stop()

    report = result["report"]
    risk = result["risk"]
    handoff = result["handoff"]

    with col_report:
        st.subheader("2. Human-confirmed fields")
        confirmed = _editable_report(st, asdict(report))
        st.caption("In the final workflow, these fields must be confirmed before saving.")
        st.json(confirmed)

    st.subheader("3. Stock-out risk and transfer action")
    risk_col, transfer_col = st.columns([1, 1])
    with risk_col:
        badge = {"red": "Red", "amber": "Amber", "green": "Green"}[risk.level]
        st.metric("Risk level", badge)
        st.metric("Days of stock", risk.days_of_stock)
        st.metric("Adjusted daily use", risk.adjusted_daily_use)
        st.write(risk.reason)
    with transfer_col:
        if risk.transfer_rank:
            st.write("Recommended transfer options")
            st.dataframe([asdict(option) for option in risk.transfer_rank], use_container_width=True)
        else:
            st.warning("No safe synthetic transfer option found.")

    st.subheader("4. Administrator handoff")
    st.success(handoff)

    with st.expander("Audit event preview"):
        st.code(json.dumps(_serialize_result(result), indent=2, default=str), language="json")
        st.caption(f"Audit events are written locally to {AUDIT_PATH.relative_to(ROOT)}.")


def _collect_source_input(st: Any, source_type: str, default_input: str) -> str:
    """Collect text, image, or audio input from the Streamlit user."""

    if source_type == "text":
        return st.text_area("Paste or edit the stock report", value=default_input, height=180)

    if source_type == "image":
        uploaded_image = st.file_uploader(
            "Upload a photographed stock card or facility report image",
            type=["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=False,
        )
        visible_text = st.text_area(
            "Type what is visible on the image, or paste OCR/Gemma vision text",
            value=default_input,
            height=140,
            help="For the public demo, the uploaded image proves device input while this text gives the extractor readable stock-card content. A real multimodal Gemma runtime can replace this hint with direct image understanding.",
        )
        if uploaded_image is None:
            st.info("Upload an image before generating the stock alert. The synthetic text below remains available for demo fallback.")
            return default_input
        image_bytes = uploaded_image.getvalue()
        st.image(uploaded_image, caption=uploaded_image.name, use_container_width=True)
        return (
            f"Uploaded image file: {uploaded_image.name}\n"
            f"Image MIME type: {uploaded_image.type}\n"
            f"Image size bytes: {len(image_bytes)}\n"
            f"Visible stock-report text: {visible_text}"
        )

    uploaded_audio = st.file_uploader(
        "Upload a short voice stock report",
        type=["wav", "mp3", "m4a", "ogg", "aac", "flac"],
        accept_multiple_files=False,
    )
    transcript_hint = st.text_area(
        "Type the spoken report transcript, or paste speech-to-text output",
        value=default_input,
        height=140,
        help="For the public demo, the uploaded audio proves device input while this transcript gives the extractor readable spoken stock-report content. A real audio Gemma runtime can replace this hint with direct audio understanding.",
    )
    if uploaded_audio is None:
        st.info("Upload an audio file before generating the stock alert. The synthetic text below remains available for demo fallback.")
        return default_input
    audio_bytes = uploaded_audio.getvalue()
    st.audio(uploaded_audio)
    return (
        f"Uploaded audio file: {uploaded_audio.name}\n"
        f"Audio MIME type: {uploaded_audio.type}\n"
        f"Audio size bytes: {len(audio_bytes)}\n"
        f"Spoken stock-report transcript: {transcript_hint}"
    )


def _editable_report(st: Any, report: dict[str, Any]) -> dict[str, Any]:
    left, right = st.columns(2)
    with left:
        report["facility"] = st.text_input("Facility", report["facility"])
        report["item"] = st.text_input("Item", report["item"])
        report["balance_units"] = st.number_input(
            "Balance units", min_value=0, value=int(report["balance_units"]), step=1
        )
    with right:
        report["average_daily_use"] = st.number_input(
            "Average daily use", min_value=1, value=int(report["average_daily_use"]), step=1
        )
        report["source_language"] = st.text_input("Source language", report["source_language"])
        report["confidence"] = st.slider("Extraction confidence", 0.0, 1.0, float(report["confidence"]))
    return report


def _serialize_result(result: dict[str, Any]) -> dict[str, Any]:
    serialized = dict(result)
    serialized["report"] = asdict(result["report"])
    serialized["risk"] = asdict(result["risk"])
    return serialized


if __name__ == "__main__":
    main()
