# HA Nostr Alert Add-on

This Home Assistant add-on allows you to send Home Assistant alerts via Nostr NIP-17 encrypted DMs.

**Note:** This code was developed with the assistance of [Goose](https://github.com/block/goose), an AI coding assistant.

## About

HA Nostr Alert is a service that listens for Home Assistant webhooks and forwards them as encrypted direct messages over the Nostr protocol. This provides a secure, decentralized way to receive notifications from your Home Assistant instance.

## Features

- Sends Home Assistant alerts via Nostr NIP-17 encrypted DMs
- Webhook listener for receiving alerts from Home Assistant
- Configurable entity monitoring
- Queue management for handling message bursts
- Support for multiple relay connections

## Installation

For detailed installation instructions, see [InstallationInstructions.md](InstallationInstructions.md).

Quick installation steps:
1. Download the add-on package (ha_nostr_alert_addon_clean.zip)
2. Extract it to a directory on your Home Assistant host
3. Add the directory as a local repository in Home Assistant Supervisor
4. Install and configure the add-on through the Home Assistant UI

## Configuration

The add-on requires the following configuration:

- `relay_urls`: List of Nostr relay URLs to connect to (in order of priority)
- `recipient_npub`: The recipient's public key (npub)
- `private_key`: Your private key (nsec)
- `monitored_entities`: List of entities to monitor
- `consolidated_entities`: List of entities to include in consolidated messages

### Multi-Relay Support (v0.1.22+)

Starting with version 0.1.22, the add-on supports multiple relays with priority-based failover:

```yaml
relay_urls:
  - "wss://relay.0xchat.com"    # Primary relay
  - "wss://relay.damus.io"      # Secondary relay
  - "wss://relay.primal.net"    # Tertiary relay
  - "wss://relay.nostr.band"    # Quaternary relay
```

The system will connect to the first available relay in the list. If the primary relay becomes unavailable, it will automatically failover to the next relay. Background health monitoring continuously checks all configured relays and attempts to reconnect to failed relays.

## Usage

After configuring the add-on, set up webhooks in Home Assistant to send alerts to the add-on's webhook endpoint.

## Support

For issues or questions, please check the documentation or open an issue on GitHub.
