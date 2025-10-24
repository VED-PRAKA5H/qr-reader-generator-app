ARG PYTHON_VERSION=3.12.1
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Create upload directory with proper permissions BEFORE switching to appuser
RUN mkdir -p /tmp/uploads && \
    chown appuser:appuser /tmp/uploads && \
    chmod 755 /tmp/uploads

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

USER appuser

# Copy with proper ownership
COPY --chown=appuser:appuser . .

EXPOSE 8000
#Developement
#CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
#Production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--timeout", "60", "app:app"]