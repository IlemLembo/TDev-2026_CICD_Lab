# Utilisation d'une image Python de base un peu ancienne pour déclencher des alertes OS
FROM python:3.14-slim

WORKDIR /app

# Copie de l'exécutable uv pour garder ton stack moderne
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copie des fichiers de configuration
COPY pyproject.toml /app/

# Installation des dépendances vulnérables via uv
# Générer un requirements.txt à la volée depuis pyproject.toml et l'installer sans builder le package
RUN uv pip compile pyproject.toml -o requirements.txt && \
    uv pip install --system --no-cache -r requirements.txt

# Copie du reste du code source
COPY . /app

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]