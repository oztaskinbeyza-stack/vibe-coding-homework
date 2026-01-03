# syntax=docker/dockerfile:1.7
##
## Tetris (Pygame) Docker Image
## - Installs SDL2 runtime libs required by pygame
## - Runs as a non-root user
## - Supports GUI via X11 forwarding (see README)
##
FROM python:3.11-slim AS runtime

# ---- Environment hardening / quality-of-life ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    # default to ALSA; can be overridden on run
    SDL_AUDIODRIVER=alsa

WORKDIR /app

# ---- OS dependencies ----
# pygame needs SDL2 + related image/mixer/ttf libs at runtime.
# Also includes libgl1 (some environments need it for windowing) and libasound2 for audio.
RUN apt-get update && apt-get install -y --no-install-recommends \
      libsdl2-2.0-0 \
      libsdl2-image-2.0-0 \
      libsdl2-mixer-2.0-0 \
      libsdl2-ttf-2.0-0 \
      libfreetype6 \
      libportmidi0 \
      libasound2 \
      libgl1 \
      libglib2.0-0 \
      libsm6 \
      libxext6 \
      libxrender1 \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ---- Non-root user ----
# Better practice than running GUI apps as root.
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# ---- Python dependencies ----
COPY --chown=appuser:appuser requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt

# ---- Application code ----
COPY --chown=appuser:appuser . /app

# Optional: document the expected port (not used here)
# EXPOSE 8080

# Default command
CMD ["python", "tetris.py"]
