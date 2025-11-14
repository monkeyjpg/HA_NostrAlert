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

- `relay_urls`: List of Nostr relay URLs to connect to (in order of priority)
- `recipient_npub`: The recipient's public key in npub format
- `private_key`: Your private key in nsec format
- `monitored_entities`: List of entity IDs to monitor for changes
- `consolidated_entities`: List of entity IDs to include in consolidated messages

#### Multi-Relay Configuration (v0.1.22+)

Starting with version 0.1.22, the add-on supports multiple relays with priority-based failover. Configure multiple relays as a list:

```yaml
relay_urls:
  - "wss://relay.0xchat.com"    # Primary relay (highest priority)
  - "wss://relay.damus.io"      # Secondary relay
  - "wss://relay.primal.net"    # Tertiary relay
  - "wss://relay.nostr.band"    # Quaternary relay (lowest priority)
recipient_npub: "npub1example..."
private_key: "nsec1example..."
monitored_entities:
  - "input_number.entity1"
  - "input_text.entity2"
consolidated_entities:
  - "input_number.entity1"
  - "input_text.entity2"
  - "input_text.entity3"
```

##### How Multi-Relay Works

1. **Priority-Based Connection**: The system attempts to connect to relays in the order they appear in the list
2. **Automatic Failover**: If the primary relay becomes unavailable, the system automatically switches to the next available relay
3. **Background Health Monitoring**: Every 5 minutes, the system checks the status of all configured relays
4. **Automatic Reconnection**: Failed relays are periodically retried (up to 3 times by default)
5. **Seamless Operation**: Message delivery continues uninterrupted during relay switches

##### Benefits

- **Improved Reliability**: No longer dependent on a single relay
- **Automatic Recovery**: Self-healing when relays become temporarily unavailable
- **Load Distribution**: Spreads connections across multiple relays
- **Reduced Downtime**: Minimizes service interruptions due to relay issues

#### Legacy Single Relay Configuration

For backward compatibility, you can still use the old single relay configuration:

```yaml
relay_url: "wss://relay.damus.io"
recipient_npub: "npub1example..."
private_key: "nsec1example..."
# ... rest of configuration
```

This will be automatically converted to a single-item relay list.

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
