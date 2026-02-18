.PHONY: dev-backend dev-frontend docker-up docker-down install-backend install-frontend lint clean

# ── Backend ──────────────────────────────────────────────
install-backend:
	cd backend && pip install -r requirements.txt

dev-backend:
	cd backend && uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# ── Frontend ─────────────────────────────────────────────
install-frontend:
	cd frontend && npm install

dev-frontend:
	cd frontend && npm start

# ── Docker ───────────────────────────────────────────────
docker-up:
	docker-compose up --build

docker-down:
	docker-compose down -v

# ── Utilities ────────────────────────────────────────────
lint:
	cd backend && python -m flake8 . --exclude=__pycache__,.venv
	cd frontend && npx eslint src/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	rm -rf frontend/build 2>/dev/null || true

# ── Database ─────────────────────────────────────────────
init-db:
	python -m backend.models.init_db
