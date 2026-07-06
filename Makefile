# RagFlow developer commands (naive RAG baseline, 2022).

.PHONY: help install dev frontend load-samples test lint format audit

help:
	@echo "install       create the venv and install dependencies (after a scan)"
	@echo "dev           run the api on :8000"
	@echo "frontend      run the streamlit ui on :8501"
	@echo "load-samples  index the bundled sample documents"
	@echo "test          run tests"
	@echo "lint          run flake8"
	@echo "format        run black and isort"
	@echo "audit         run pip-audit on requirements.txt"

install:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

dev:
	. .venv/bin/activate && uvicorn src.api.main:app --reload --port 8000

frontend:
	. .venv/bin/activate && streamlit run frontend/streamlit_app.py --server.port 8501

load-samples:
	. .venv/bin/activate && python scripts/load_sample_data.py

test:
	. .venv/bin/activate && pytest tests -q

lint:
	. .venv/bin/activate && flake8 src

format:
	. .venv/bin/activate && black src tests && isort src tests

audit:
	. .venv/bin/activate && pip-audit -r requirements.txt
