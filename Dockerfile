ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

# Install Python, pip, and jq
RUN apk add --no-cache python3 py3-pip jq bash

# Copy files
COPY requirements.txt /
COPY src/ /src/

# Install Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r /requirements.txt

# Copy rootfs for s6-overlay service structure
COPY rootfs /

# Labels for Home Assistant
LABEL \
  io.hass.version="0.1.20" \
  io.hass.type="addon" \
  io.hass.arch="armhf|armv7|aarch64|amd64|i386"
