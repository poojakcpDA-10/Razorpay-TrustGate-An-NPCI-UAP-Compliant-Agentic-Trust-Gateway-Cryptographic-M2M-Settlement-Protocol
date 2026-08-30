#!/usr/bin/env bash
# Starts the Streamlit frontend on http://localhost:8501
set -e
cd "$(dirname "$0")"
export BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
streamlit run frontend/Home.py
