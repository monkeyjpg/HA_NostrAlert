ARG BUILD_FROM
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

# Labels for Home Assistant
LABEL \
  io.hass.version="0.1.0" \
  io.hass.type="addon" \
  io.hass.arch="armhf|armv7|aarch64|amd64|i386"

CMD [ "/run.sh" ]
