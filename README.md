# HA Nostr Alert

Home Assistant add-on for sending alerts via Nostr NIP-17 encrypted DMs.

## Overview

This standalone service listens for Home Assistant webhook calls and sends alerts via Nostr NIP-17 encrypted direct messages. It's designed to work with the HA_EMS (Home Assistant Energy Management System) but can be configured for any Home Assistant entities.

## Features

- Sends encrypted DMs using Nostr NIP-17 protocol
- Listens for Home Assistant state changes via webhooks
- Consolidates related entity information into single alerts
- Message queuing for offline scenarios
- YAML-based configuration
- Health check endpoint

## Requirements

- Python 3.8+
- Home Assistant instance
- Nostr relay (e.g., Haven running locally)
- `nostr-sdk` Python bindings
- Flask for webhook server

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/HA_nostrAlert.git
   cd HA_nostrAlert
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the service (see Configuration section below)

4. Run the service:
   ```bash
   python src/main.py
   ```

## Configuration

Create a `config.yaml` file in the root directory:

```yaml
nostr:
  relay_url: "wss://relay.damus.io"  # Your Nostr relay URL
  recipient_npub: "npub1..."         # Recipient's public key
  private_key: "nsec1..."            # Sender's private key

alerts:
  monitored_entities:
    - "input_number.logic_pwrlimit"
    - "input_text.logic_m1_switch"
  consolidated_entities:
    - "input_number.logic_pwrlimit"
    - "input_text.logic_m1_switch"
    - "input_text.logic_m1_logstring"

queue:
  max_size: 5
```

## Home Assistant Integration

Add this to your Home Assistant `configuration.yaml`:

```yaml
# Webhook automation to send entity state changes
automation:
  - alias: "Send Nostr Alert on Entity Change"
    trigger:
      - platform: state
        entity_id:
          - input_number.logic_pwrlimit
          - input_text.logic_m1_switch
    action:
      - service: rest_command.send_nostr_alert
        data:
          entity_id: "{{ trigger.entity_id }}"
          new_state: "{{ trigger.to_state }}"

# REST command to send webhook
rest_command:
  send_nostr_alert:
    url: "http://localhost:5000/webhook"
    method: POST
    payload: >
      {
        "entity_id": "{{ entity_id }}",
        "new_state": {{ new_state | to_json }}
      }
    content_type: "application/json"
```

## API Endpoints

- `POST /webhook` - Receive Home Assistant state changes
- `GET /health` - Health check endpoint

## Development

### Project Structure

```
HA_nostrAlert/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── main.py            # Main entry point
│   ├── webhook_server.py  # Flask webhook server
│   ├── nostr_client.py    # Nostr client implementation
│   └── message_processor.py # Message processing and consolidation
├── requirements.txt       # Python dependencies
├── config.yaml           # Configuration file
├── README.md             # This file
├── analysis_usecase.md   # Requirements analysis
└── todo.md              # Development todo list
```

### Running Tests

```bash
python -m pytest tests/
```

## Security Considerations

- Store your Nostr private key securely
- Use TLS/SSL for relay connections when possible
- Validate all incoming webhook data
- Limit queue size to prevent memory issues

## License

MIT License - see LICENSE file for details.
