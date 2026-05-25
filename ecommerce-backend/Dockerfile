FROM python:3.13.7-alpine AS base
RUN addgroup -S myuser && adduser -S -G myuser myuser

USER myuser

COPY --from=ghcr.io/astral-sh/uv:0.11.15 /uv /uvx /bin/
# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image
COPY --chown=myuser:myuser . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "80"]
