"""Streamlit entry point for the AfyaFlow Pwani demo application.

The interactive workflow will be implemented after the domain contracts,
risk engine, and Gemma tool-calling path are tested.
"""

from __future__ import annotations


def main() -> None:
    """Display a placeholder message until the judged workflow is implemented."""
    try:
        import streamlit as st
    except ModuleNotFoundError as exc:  # pragma: no cover - defensive runtime guidance
        raise SystemExit(
            "Streamlit is not installed. Install app dependencies with: "
            "python -m pip install -e .[app]"
        ) from exc

    st.set_page_config(page_title="AfyaFlow Pwani", page_icon="🏥", layout="wide")
    st.title("AfyaFlow Pwani")
    st.caption("Gemma 4 assistant for early stock-out warnings in frontline health centres.")
    st.info("The full report-to-alert workflow will be added in the application milestone.")


if __name__ == "__main__":
    main()
