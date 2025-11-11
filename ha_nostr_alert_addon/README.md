# HA Nostr Alert Add-on

This Home Assistant add-on allows you to send Home Assistant alerts via Nostr NIP-17 encrypted DMs.

## About

HA Nostr Alert is a service that listens for Home Assistant webhooks and forwards them as encrypted direct messages over the Nostr protocol. This provides a secure, decentralized way to receive notifications from your Home Assistant instance.

## Features

- Sends Home Assistant alerts via Nostr NIP-17 encrypted DMs
- Webhook listener for receiving alerts from Home Assistant
- Configurable entity monitoring
- Queue management for handling message bursts
- Support for multiple relay connections

## Installation

1. Navigate to the Supervisor panel in Home Assistant
2. Go to Add-ons
3. Click on the "+" button to add a new repository
4. Enter the repository URL
5. Find "HA Nostr Alert" in the add-on store
6. Click "Install"
7. Configure the add-on with your Nostr settings
8. Start the add-on

## Configuration

The add-on requires the following configuration:

- `relay_url`: The Nostr relay URL to connect to
- `recipient_npub`: The recipient's public key (npub)
- `private_key`: Your private key (nsec)
- `monitored_entities`: List of entities to monitor
- `consolidated_entities`: List of entities to include in consolidated messages

## Usage

After configuring the add-on, set up webhooks in Home Assistant to send alerts to the add-on's webhook endpoint.

## Support

For issues or questions, please check the documentation or open an issue on GitHub.
