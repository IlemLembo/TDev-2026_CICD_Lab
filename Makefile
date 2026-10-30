.PHONY: help install migrate run lint security clean

help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Installe les dépendances avec uv
	uv sync

init-db: ## Applique les migrations et peuple la base avec des données de démo
	uv run python manage.py makemigrations
	uv run python manage.py migrate
	uv run python manage.py seed_data

clear-db: ## Supprime la base de données et les fichiers de migration
	rm -f db.sqlite3
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

migrate: ## Applique les migrations de la base de données
	uv run python manage.py makemigrations
	uv run python manage.py migrate

create_superuser: ## Crée un superutilisateur Django
	uv run python manage.py createsuperuser

run: ## Lance le serveur de développement Django
	uv run python manage.py runserver 0.0.0.0:8000

lint: ## Analyse le code avec Semgrep (si installé)
	uv run ruff format --

clean: ## Nettoie les fichiers temporaires et la base de données de test
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f db.sqlite3

clear-env:
	rm -rf .venv

safety: ## Lance un scan de vulnérabilités des dépendances avec Safety
	uv run safety check

ruff: ## Lance un scan de style de code avec Ruff
	uv run ruff check .

semgrep: ## Lance un scan de sécurité avec Semgrep
	uv run semgrep scan --config auto

trivy:
	docker build -t tdev-2026-cicd-lab:latest .
	trivy image tdev-2026-cicd-lab:latest

install-trivy:
	curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh -s -- -b /usr/local/bin v0.76.1

check-v0:
	git checkout v0-Very-Bad-way-toDo

check-linting-only:
	uv add ruff
	uv run ruff check .
	uv run ruff format --check .

fix-linting-only:
	uv run ruff format --fix .
	uv run ruff check .
	uv run ruff format --check .

