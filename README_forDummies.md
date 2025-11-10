# HA Nostr Alert - Simple Explanation

This document explains the HA Nostr Alert system in simple terms for non-programmers like business analysts or product owners. It describes what each component does and how they work together.

## What Does This System Do?

HA Nostr Alert is a notification system that sends alerts from your smart home (Home Assistant) to your phone or computer via a secure messaging network called Nostr. When specific things happen in your smart home, like a power limit changing or a switch turning on/off, you get an instant secure message.

## System Components Explained

### 1. Configuration Manager (`config.py`)
Think of this as the system's "settings panel" or "control center".
- **What it does**: Reads and manages all the settings from the `config.yaml` file
- **Examples of settings**:
  - Where to send messages (Nostr relay URL)
  - Who receives messages (recipient's public key)
  - Which smart home devices to watch
  - How many messages to save when offline

### 2. Webhook Server (`webhook_server.py`)
Think of this as the system's "mailbox" or "front door".
- **What it does**: Listens for incoming messages from your smart home system
- **How it works**: When a smart home device changes (like a switch flips), Home Assistant sends a message to this system through a specific internet address
- **Security**: Only accepts messages from trusted sources

### 3. Nostr Client (`nostr_client.py`)
Think of this as the system's "secure messenger" or "mail carrier".
- **What it does**: Sends encrypted (secret) messages through the Nostr network
- **How it works**: 
  - Connects to a Nostr relay (like a post office)
  - Encrypts messages so only the intended recipient can read them
  - Sends messages securely using NIP-17 protocol (a special secure messaging standard)
- **Features**:
  - Automatically retries if connection fails
  - Maintains secure connections

### 4. Message Processor (`message_processor.py`)
Think of this as the system's "message editor" or "consolidator".
- **What it does**: Takes incoming alerts and makes them more useful
- **How it works**:
  - Collects multiple alerts that happen at the same time
  - Combines related information into one comprehensive message
  - Example: Instead of getting three separate messages about power changes, you get one message with all the related information
  - Manages a queue of messages in case the internet goes down temporarily

### 5. Main Application (`main.py`)
Think of this as the system's "orchestrator" or "conductor".
- **What it does**: Brings all components together and manages the overall operation
- **How it works**:
  - Starts all subsystems when the program begins
  - Keeps everything running smoothly
  - Shuts everything down cleanly when needed
  - Acts as the central coordinator between all components

## How It All Works Together - A Real-World Example

1. **Trigger**: Your smart home energy system changes the power limit from 1000W to 800W
2. **Detection**: Home Assistant notices this change and sends a message to our system's "mailbox" (`webhook_server.py`)
3. **Queue**: The message goes into a holding area (`message_processor.py`) where it waits with any other recent changes
4. **Consolidation**: Our system checks if there are other related changes (maybe a switch also flipped) and combines them into one comprehensive message
5. **Secure Sending**: The combined message gets encrypted and sent through the Nostr network (`nostr_client.py`) to your phone
6. **Delivery**: You receive a single secure message saying "Power limit changed to 800W, Switch is now ON, Log shows normal operation"

## Why This Approach?

1. **Privacy**: Messages are encrypted end-to-end - no one except you can read them
2. **Reliability**: If internet drops, messages are saved and sent when connection returns
3. **Efficiency**: Related alerts are combined into one meaningful message instead of multiple notifications
4. **Flexibility**: Easy to configure which devices to monitor and how to handle alerts
5. **Standards-Based**: Uses established Nostr protocols for secure messaging

## Key Benefits

- **Instant Notifications**: Get real-time alerts about important smart home events
- **Secure Communication**: Military-grade encryption keeps your information private
- **Smart Consolidation**: Related events are grouped together for better understanding
- **Offline Resilience**: Messages are saved when internet is down and sent later
- **Easy Configuration**: Simple text file controls all settings
- **Open Standards**: Built on widely-adopted Nostr protocol

This system transforms raw smart home data into meaningful, secure, and timely notifications that help you stay informed about your home's operations.
