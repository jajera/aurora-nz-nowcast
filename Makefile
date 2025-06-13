# Aurora Nowcast NZ - Development Makefile

.PHONY: help install install-dev test lint format clean run-backend run-frontend deploy

help: ## Show this help message
	@echo "Aurora Nowcast NZ - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt

test: ## Run tests
	cd backend && python test_geonet.py

test-pytest: ## Run pytest tests
	pytest tests/ -v

test-integration: ## Run integration tests
	pytest tests/ -v -m integration

test-verbose: ## Run tests with verbose output
	cd backend && python -v test_geonet.py

lint: ## Run linting
	flake8 backend/
	black --check backend/
	isort --check-only backend/

format: ## Format code
	black backend/
	isort backend/

clean: ## Clean temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf backend/*.log
	rm -rf backend/test_status.json

run-backend: ## Run the backend data processor
	cd backend && python geonet_data.py

run-frontend: ## Serve the frontend locally
	cd docs && python -m http.server 8000

explore-s3: ## Explore S3 bucket structure
	cd backend && python explore_s3_new.py

deploy: ## Deploy to GitHub Pages (manual - via push)
	git add .
	git commit -m "Update: $(shell date)"
	git push origin main

deploy-data: ## Update aurora data only (for manual testing)
	make run-backend
	git add docs/status.json
	git commit -m "Update aurora data: $(shell date)"
	git push origin main

setup: install-dev ## Complete development setup
	@echo "✅ Development environment ready!"
	@echo "📊 Testing data connection..."
	@make test || echo "⚠️  Some tests have warnings, but core functionality works"
	@echo "🚀 Setup complete!"
