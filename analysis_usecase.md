# Use Case Analysis: Home Assistant Nostr Alert Integration

## Project Overview
This project aims to create a Home Assistant add-on that sends alerts as encrypted Direct Messages (DM) through the Nostr protocol using NIP-17. The integration will allow Home Assistant users to receive real-time notifications directly to their Nostr clients.

Based on our discussion and review of the HA_EMS system, we'll focus on creating a generic alert system that can send notifications when specific Home Assistant entities change, with our first use case being alerts for M1 Power Limit and Active Status changes.

## Core Requirements Analysis

### Requirement 1: Home Assistant Integration Approach
After analyzing the options, here are the pros and cons of each approach:

**Option A: Home Assistant Custom Component (Notify Platform)**
Pros:
- Native integration with Home Assistant notification system
- Can be used with existing alert automations
- Appears in HA's notification integrations list
- Direct access to HA's entity state management
- Can leverage HA's configuration validation

Cons:
- More complex development process
- Requires understanding of HA's component architecture
- Need to handle HA's async event loop properly
- More challenging to distribute outside official channels

**Option B: Standalone Add-on with Webhook/API Interface**
Pros:
- Easier to develop, test, and deploy independently
- Can be shared more easily as a standalone package
- Simpler development workflow
- Can be updated without affecting HA core
- Better isolation from HA internals

Cons:
- Requires additional configuration steps
- Need to manage communication between HA and add-on
- Slightly more complex setup for end users

**Recommendation:** We'll go with Option B (Standalone Add-on) as it's more suitable for sharing with other users and easier to develop and maintain.

### Requirement 2: Nostr Client Library Selection
For Python-based Nostr implementation with NIP-17 support:

**Recommended Library: `nostr-sdk` with Python bindings**
Pros:
- Full NIP-17 support for secure DMs
- Well-maintained and actively developed
- Comprehensive feature set including encryption
- Good documentation and community support
- Robust relay connection management
- Supports both NIP-04 and NIP-17 encryption methods

Alternative: Pure Python libraries like `python-nostr`
Pros:
- Pure Python, no external dependencies
- Simpler installation
Cons:
- Limited NIP-17 support
- Less actively maintained

**Decision:** We'll use `nostr-sdk` with Python bindings for its comprehensive NIP-17 support and robust feature set.

### Requirement 3: Initial Alert Scope - M1 Power Limit and Active Status Changes
Based on the HA_EMS documentation, we'll focus on monitoring these specific entities:
- `input_number.logic_pwrlimit` - Power limit value (1708W, 2700W, 3300W)
- `input_text.logic_m1_switch` - Active status ('on' or 'off')
- `input_text.logic_m1_logstring` - Log entry for full documentation

## Detailed Requirements Specification

### Functional Requirements

1. **Nostr Communication**
   - Send encrypted DMs using NIP-17 protocol
   - Connect to configurable Nostr relay (including local relays like Haven)
   - Support for recipient npub configuration
   - Handle relay connection errors gracefully
   - Implement proper event signing with private key

2. **Home Assistant Integration**
   - Monitor specific Home Assistant entities for state changes
   - Accept entity IDs as configuration parameters
   - Send alerts when monitored entities change state
   - Include entity ID, old value, new value, and timestamp in alerts
   - Support for custom alert messages with template variables

3. **Configuration Management**
   - YAML-based configuration file
   - Configurable relay URL
   - Recipient npub specification
   - Monitored entity list with optional custom messages
   - Private key storage with basic security measures

4. **Security Requirements**
   - Secure storage of Nostr private key (file permissions, basic encryption)
   - Validation of Nostr public keys (npub format)
   - Secure relay connections (TLS/SSL support)
   - Input validation for all configuration parameters

5. **Error Handling**
   - Graceful handling of relay connection failures
   - Retry mechanism for failed message delivery
   - Logging of errors and warnings
   - Health check endpoint for monitoring

### Non-Functional Requirements

1. **Performance**
   - Low latency message delivery (< 1 second typical)
   - Minimal resource usage (CPU, memory)
   - Efficient relay connection management

2. **Reliability**
   - Message queuing for offline relay scenarios
   - Automatic reconnect to relay after disconnection
   - Persistent storage of unsent messages

3. **Usability**
   - Clear documentation with setup examples
   - Informative logging for troubleshooting
   - Simple configuration format

### Technical Architecture

1. **Core Components**
   - Nostr client module (using nostr-sdk)
   - Home Assistant webhook listener
   - Configuration manager
   - Message formatter
   - Relay connection manager

2. **Data Flow**
   ```
   Home Assistant State Change 
   → Webhook Call to Add-on 
   → Message Formatting 
   → Nostr Event Creation 
   → Relay Publishing 
   → Recipient Notification
   ```

3. **Configuration Example**
   ```yaml
   nostr:
     relay_url: "ws://localhost:6969"  # Haven relay
     recipient_npub: "npub1..."       # Target recipient
     private_key: "nsec1..."          # Sender private key (securely stored)
   
   alerts:
     - entity_id: "input_number.logic_pwrlimit"
       message_template: "Power limit changed to {{ new_state.state }}W"
     
     - entity_id: "input_text.logic_m1_switch"
       message_template: "M1 status changed to {{ new_state.state }}"
       
     - entity_id: "input_text.logic_m1_logstring"
       message_template: "System log: {{ new_state.state }}"
   ```

## Implementation Plan

### Phase 1: Core Nostr Integration
1. Set up nostr-sdk with Python bindings
2. Implement NIP-17 DM sending functionality
3. Create basic relay connection management
4. Develop key management with secure storage

### Phase 2: Home Assistant Integration
1. Create webhook endpoint for receiving HA state changes
2. Implement entity monitoring logic for logic_pwrlimit and logic_m1_switch
3. Develop message consolidation system (pwrlimit + switch + logstring)
4. Add configuration management with YAML

### Phase 3: Error Handling and Reliability
1. Implement message queue with limit (default 5)
2. Add retry mechanism for failed message delivery
3. Implement graceful handling of relay connection failures
4. Set up logging of errors and warnings

### Phase 4: Testing and Refinement
1. Integration testing with HA_EMS system
2. Error handling and edge case testing
3. Documentation and example configurations
4. Security review

## Expanded Requirements Analysis and Use Cases

### Brainstorming Additional Use Cases

Based on our discussion, let's expand our thinking beyond the initial M1 Power Limit and Active Status alerts:

1. **Generic Entity State Change Alerts**
   - Any Home Assistant entity (sensor, switch, input_number, etc.)
   - Configurable triggering conditions (state changes, specific value thresholds)
   - Template-based message formatting

2. **System Health Monitoring**
   - Home Assistant restart notifications
   - Add-on status alerts
   - Backup completion notifications
   - Storage space warnings

3. **Security and Access Alerts**
   - Door/window sensor triggers
   - Motion detection alerts
   - Alarm system status changes
   - Failed login attempts

4. **Environmental Monitoring**
   - Temperature/humidity threshold alerts
   - Leak detection notifications
   - Air quality warnings
   - Weather event alerts

5. **Energy Management Notifications** (from HA_EMS)
   - Solar production milestones
   - Battery charge level alerts
   - Grid interaction notifications
   - Cost savings reports

6. **Integration Status Alerts**
   - IoT device offline notifications
   - API connection status
   - Third-party service availability

### Prioritization for Releases

**Release 1 (MVP - Minimum Viable Product):**
- Core Nostr NIP-17 DM sending capability
- Basic Home Assistant webhook integration
- Single recipient support
- Configuration via YAML file
- Secure private key storage
- Error handling and logging

**Release 2 (Enhanced Functionality):**
- Template-based message formatting
- Multiple entity monitoring
- Rate limiting controls
- Offline message queuing
- Enhanced configuration options

**Release 3 (Advanced Features):**
- Multiple recipient support
- Bi-directional communication capabilities
- Integration with Home Assistant notification system
- Advanced filtering and routing

### Detailed Analysis of Home Assistant Alert Integration

To answer your first question about setting up Nostr alerts the same way as mobile alerts, we need to understand how Home Assistant's alert system works:

1. **Native Alert Integration Approach:**
   - Create a custom `notify` platform that integrates directly with HA's notification system
   - This would appear in the "Notifications" section of HA settings
   - Users could configure alerts using HA's native UI or YAML
   - Would work with existing `alert` integrations seamlessly

2. **Current Mobile Alert Setup:**
   - Mobile app registers as a notification service
   - Users configure alerts to send to `notify.mobile_app_<device>`
   - Supports templates, grouping, and rich notifications

For a similar experience with Nostr, we would need to implement a custom component rather than a standalone add-on.

### Class Diagram Concept

Let me propose a conceptual class diagram for the relationships:

```
┌─────────────────┐          ┌──────────────────┐
│   NostrClient   │◄─────────┤  NostrRecipient  │
└─────────────────┘    1..*  └──────────────────┘
        │                            │
        │                            │
        ▼                            ▼
┌─────────────────┐          ┌──────────────────┐
│   NostrEvent    │          │    PublicKey     │
└─────────────────┘          └──────────────────┘
        │
        │
        ▼
┌─────────────────┐
│   RelayManager  │
└─────────────────┘
        │
        │
        ▼
┌─────────────────┐
│   Configuration │
└─────────────────┘

┌─────────────────┐          ┌──────────────────┐
│ HomeAssistant   │◄─────────┤  EntityState     │
└─────────────────┘    1..*  └──────────────────┘
        │                            │
        │                            │
        ▼                            ▼
┌─────────────────┐          ┌──────────────────┐
│  WebhookServer  │          │   EntityConfig   │
└─────────────────┘          └──────────────────┘
        │
        │
        ▼
┌─────────────────┐
│ AlertDispatcher │
└─────────────────┘
        │
        │
        ▼
┌─────────────────┐
│ MessageTemplate │
└─────────────────┘
```

### Bidirectional Communication Analysis

Regarding your second question about receiving DMs from a defined recipient:

**Benefits:**
- Secure two-way communication channel
- Delivery confirmation receipts
- Remote command/control possibilities
- Status queries ("ping" functionality)

**Implementation Considerations:**
- Need to listen for incoming events on the relay
- Message filtering to only process from trusted sources
- Command parsing and execution framework
- Security implications of remote control capabilities

**Potential Use Cases:**
- Acknowledgment of received alerts
- Requesting system status information
- Remote triggering of automations
- Configuration updates

**Security Concerns:**
- Need robust authentication of command sources
- Rate limiting to prevent abuse
- Logging of all received commands
- Granular permission controls

### NWC Integration with Cashu Wallet

For your third question about NWC (Nostr Wallet Connect) and Cashu wallet integration:

**Benefits:**
- Enable payments for premium relay services
- Micropayments for advanced features
- Support for paid Nostr services
- Future monetization possibilities

**Technical Considerations:**
- NWC implementation complexity
- Cashu wallet integration specifics
- Payment request/response handling
- Balance tracking and management

**Implementation Phases:**
1. Basic NWC connection establishment
2. Payment request generation
3. Payment verification and processing
4. Integration with relay selection/payment logic

### Updated Requirements Based on Clarification

1. **Architecture Decision**: We'll proceed with the standalone add-on approach with webhook interface for Home Assistant integration.

2. **Bidirectional Communication**: Receiving DMs from trusted sources is noted as a future idea but not part of the current plan.

3. **NWC Integration**: Wallet integration is also noted as a future possibility but not part of the initial implementation.

4. **Deployment Model**: The add-on will be deployed as a standalone service on your home laptop.

5. **Message Formatting**: Initially, we'll focus on simple messages, with the capability to send consolidated information. Specifically, when there is a change in `logic_pwrlimit` or `logic_m1_switch`, we'll send a DM with the current values of `logic_pwrlimit`, `logic_m1_switch`, and `logic_m1_logstring`.

6. **Error Recovery**: Messages will be queued up to a limit (default 5) when the relay is offline, with retry mechanism upon reconnection.

### Refined Technical Requirements

Based on these clarifications, our technical approach will be:

1. **Standalone Add-on**: A Python-based service that runs independently of Home Assistant but communicates via webhooks.

2. **Webhook Interface**: Will listen for POST requests from Home Assistant containing entity state changes.

3. **Message Consolidation**: When specific entities change, the system will gather related information and send a consolidated message.

4. **Message Queue**: Implementation of an in-memory queue with configurable limit (default 5 messages) to handle offline scenarios.

5. **Nostr Protocol**: Full implementation of NIP-17 for secure DMs using the nostr-sdk Python bindings.

6. **Configuration**: YAML-based configuration file with options for relay URL, recipient npub, private key, and queue settings.
