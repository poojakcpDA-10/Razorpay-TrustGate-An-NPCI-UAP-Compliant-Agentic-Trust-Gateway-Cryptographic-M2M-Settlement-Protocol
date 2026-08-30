#!/usr/bin/env bash
# Starts the FastAPI backend on http://localhost:8000
set -e
cd "$(dirname "$0")"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
