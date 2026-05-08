FROM python:3.14-slim-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .

FROM python:3.14-slim-bookworm
COPY --from=builder /app /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
EXPOSE 8000
RUN uv run manage.py collectstatic --noinput
CMD ["uv", "run", "gunicorn", "tac_hydro.wsgi:application", "--workers", "8", "--bind", "0.0.0.0:8000"]
