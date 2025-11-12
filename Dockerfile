ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

# Install Python, pip, and jq
RUN apk add --no-cache python3 py3-pip jq bash

# Copy files
COPY requirements.txt /
COPY src/ /src/
COPY run.sh /

# Install Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r /requirements.txt

# Make run script executable
RUN chmod a+x /run.sh

# Set the working directory
WORKDIR /

# Define the command to run the application
ENTRYPOINT [ "/run.sh" ]

# Labels for Home Assistant
LABEL \
  io.hass.version="0.1.7" \
  io.hass.type="addon" \
  io.hass.arch="armhf|armv7|aarch64|amd64|i386"
