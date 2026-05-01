.PHONY: help build up down logs restart seed clean

# Default target
help: ## Show this help
	@echo "═══════════════════════════════════════════════"
	@echo "  🍽️  Slooze Food Ordering Platform"
	@echo "═══════════════════════════════════════════════"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ─── Docker Commands ─────────────────────────────────────────────────

build: ## Build all Docker containers
	docker-compose build

up: ## Start all services in background
	docker-compose up -d

up-logs: ## Start all services with logs
	docker-compose up

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

logs: ## View logs for all services
	docker-compose logs -f

logs-backend: ## View backend logs
	docker-compose logs -f backend

logs-frontend: ## View frontend logs
	docker-compose logs -f frontend

# ─── Development ─────────────────────────────────────────────────────

dev-backend: ## Start backend in development mode
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Start frontend in development mode
	cd frontend && npm run dev

dev-db: ## Start only database and Redis
	docker-compose up -d postgres redis

# ─── Database ────────────────────────────────────────────────────────

seed: ## Seed the database with test data
	cd backend && python -m app.database.seed

migrate: ## Run database migrations
	cd backend && alembic upgrade head

migration: ## Create a new migration
	cd backend && alembic revision --autogenerate -m "$(msg)"

# ─── Cleanup ─────────────────────────────────────────────────────────

clean: ## Remove all containers and volumes
	docker-compose down -v --remove-orphans

prune: ## Full cleanup including images
	docker-compose down -v --rmi all --remove-orphans
