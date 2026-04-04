FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy only the files needed for installation to cache the layer
COPY pyproject.toml uv.lock .python-version ./

# Install dependencies (this creates the .venv)
RUN uv sync --frozen --no-install-project --no-dev

# Final Stage
FROM python:3.12-slim-bookworm
WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/
COPY main.py .

# Use the virtual environment's python
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "main.py"]