.PHONY: setup api demo reset test data train eval

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r api/requirements.txt
	@echo "ml owner sets up"
	@echo "web owner sets up"
	@echo "contracts owner sets up"

api:
	.venv/bin/uvicorn api.main:app --reload --port 8000

demo:
	@.venv/bin/uvicorn api.main:app --reload --port 8000 & api_pid=$$!; \
	trap 'kill $$api_pid 2>/dev/null || true' EXIT INT TERM; \
	if [ -f web/package.json ]; then cd web && pnpm dev; \
	else echo "web/package.json absent; owner sets up"; wait $$api_pid; fi

reset:
	curl -X POST localhost:8000/v1/sim/reset

test:
	pytest api

data train eval:
	@if [ -f ml/Makefile ]; then $(MAKE) -C ml $@; else echo "ml owner sets up $@"; fi
