# HA Nostr Alert Add-on Documentation

## Installation

1. Navigate in your Home Assistant frontend to **Supervisor** -> **Add-on Store**.
2. Find the "HA Nostr Alert" add-on and click it.
3. Click on the "INSTALL" button.

## How to use

### Initial setup

1. Start the "HA Nostr Alert" add-on.
2. Check the logs of the "HA Nostr Alert" add-on to see if everything went well.
3. Set up webhooks in Home Assistant to send alerts to the add-on.

### Configuration

The add-on requires the following configuration parameters:

#### Basic Configuration

- `relay_url`: The Nostr relay URL to connect to (e.g., `wss://relay.damus.io`)
- `recipient_npub`: The recipient's public key in npub format
- `private_key`: Your private key in nsec format
- `monitored_entities`: List of entity IDs to monitor for changes
- `consolidated_entities`: List of entity IDs to include in consolidated messages

#### Example configuration

```yaml
relay_url: "wss://relay.damus.io"
recipient_npub: "npub1example..."
private_key: "nsec1example..."
monitored_entities:
  - "input_number.logic_pwrlimit"
  - "input_text.logic_m1_switch"
consolidated_entities:
  - "input_number.logic_pwrlimit"
  - "input_text.logic_m1_switch"
  - "input_text.logic_m1_logstring"
```

### Setting up webhooks in Home Assistant

To send alerts to the add-on, configure webhooks in your Home Assistant automation:

```yaml
automation:
  - alias: "Send alert via Nostr"
    trigger:
      # Your trigger conditions
    action:
      - service: webhook.call
        data:
          webhook_id: "ha_nostr_alert"
          payload: "{{ states }}"
```

The add-on listens on port 5000 for incoming webhook requests.

## Support

For issues or questions:

1. Check the add-on logs in Home Assistant
2. Review the configuration settings
3. Open an issue on the GitHub repository if the problem persists

## Troubleshooting

### Common issues

1. **Connection problems**: Verify the relay URL is correct and accessible.
2. **Authentication failures**: Check that your private key and recipient's public key are in the correct format.
3. **No messages received**: Ensure the monitored entities are correctly configured and changing state.

### Checking logs

View the add-on logs in Home Assistant to diagnose issues:

1. Navigate to **Supervisor** -> **Add-on Store**
2. Click on "HA Nostr Alert"
3. Click on the "Logs" tab

Look for error messages or warnings that might indicate the cause of any problems.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.
