# tools-base.Dockerfile
# Base image for Python tools and benchmark scripts

FROM python:3.11-slim

# ----------------------------
# Set working directory
# ----------------------------
WORKDIR /workspace

# ----------------------------
# Install OS dependencies
# ----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    wget \
    curl \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Create a non-root user
# ----------------------------
RUN useradd -ms /bin/bash developer
USER developer

# ----------------------------
# Python environment
# ----------------------------
ENV VENV_PATH=/workspace/venv
RUN python3 -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

# ----------------------------
# Install Python dependencies (optional: can also be done at runtime)
# ----------------------------
COPY requirements.txt /workspace/
RUN pip install --upgrade pip && pip install -r requirements.txt

# ----------------------------
# Default command keeps container alive for interactive use
# ----------------------------
CMD ["tail", "-f", "/dev/null"]
