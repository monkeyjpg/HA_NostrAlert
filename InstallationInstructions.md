# Installing HA Nostr Alert Add-on Locally

This guide will walk you through installing the HA Nostr Alert add-on on your local Home Assistant instance for testing purposes.

## Prerequisites

1. A running Home Assistant instance with Supervisor
2. Access to the Home Assistant filesystem
3. Basic knowledge of Home Assistant add-ons

## Installation Steps

### 1. Prepare the Add-on Files

First, you need to prepare the add-on files in a directory structure that Home Assistant can recognize:

```
local-addon-repo/
├── config.yaml
├── Dockerfile
├── run.sh
├── README.md
├── DOCS.md
├── CHANGELOG.md
├── requirements.txt
└── src/
    ├── __init__.py
    ├── config.py
    ├── main.py
    ├── webhook_server.py
    ├── nostr_client.py
    └── message_processor.py
```

### 2. Copy Files to Home Assistant

Copy the entire `local-addon-repo` directory to your Home Assistant instance. The recommended location is:

```
/share/local-addon-repo/
```

You can do this using:
- The Terminal add-on in Home Assistant
- SSH access to your Home Assistant host
- File sharing mechanisms like SMB if available

Example using the Terminal add-on:
```bash
# Create the directory structure
mkdir -p /share/local-addon-repo

# Copy files (you'll need to transfer them from your development machine)
# This can be done using wget, curl, or scp depending on your setup
```

### 3. Add Local Repository to Home Assistant

1. Navigate to your Home Assistant frontend
2. Go to **Supervisor** > **Add-on Store**
3. Click on the three dots menu (⋮) in the top right
4. Select **Repositories**
5. Click the **Add** button
6. Enter the URL to your Git repository:
   ```
   https://github.com/yourusername/HA_nostrAlert.git
   ```
7. Click **Add**

### 4. Install the Add-on

1. Refresh the Add-on Store page
2. You should now see "HA Nostr Alert" in the list of available add-ons
3. Click on the "HA Nostr Alert" add-on
4. Click **Install**
5. Wait for the installation to complete

### 5. Configure the Add-on

1. After installation, click on **Configuration** tab
2. Fill in the required configuration parameters:
   - `relay_url`: Your Nostr relay URL (e.g., `wss://relay.damus.io`)
   - `recipient_npub`: The recipient's public key in npub format
   - `private_key`: Your private key in nsec format
   - `monitored_entities`: List of entity IDs to monitor
   - `consolidated_entities`: List of entity IDs to include in consolidated messages

Example configuration:
```yaml
relay_url: "wss://relay.damus.io"
recipient_npub: "npub1yourrecipientkeyhere"
private_key: "nsec1yourprivatekeyhere"
monitored_entities:
  - "input_number.logic_pwrlimit"
  - "input_text.logic_m1_switch"
consolidated_entities:
  - "input_number.logic_pwrlimit"
  - "input_text.logic_m1_switch"
  - "input_text.logic_m1_logstring"
```

### 6. Start the Add-on

1. Click **Save** to save your configuration
2. Click **Start** to start the add-on
3. Check the **Log** tab to ensure the add-on starts without errors

### 7. Test with a Sample Webhook

To test the add-on, you can send a sample webhook request to trigger a Nostr message:

1. In Home Assistant, go to **Developer Tools** > **Services**
2. Find the `webhook.call` service
3. Call the service with the following parameters:
   ```yaml
   webhook_id: "ha_nostr_alert"  # This is the default webhook endpoint
   payload: '{"entity_id": "sensor.test", "state": "on", "attributes": {"friendly_name": "Test Sensor"}}'
   ```

Alternatively, you can use curl from another machine to send a POST request to your Home Assistant instance:

```bash
curl -X POST \
  http://YOUR_HOME_ASSISTANT_IP:8123/api/webhook/ha_nostr_alert \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "sensor.test", "state": "on", "attributes": {"friendly_name": "Test Sensor"}}'
```

### 8. Verify Operation

1. Check the add-on logs in Home Assistant to see if the webhook was received
2. Monitor your Nostr client to see if you receive the encrypted DM
3. Look for any error messages in the logs that might indicate issues

## Troubleshooting

### Common Issues

1. **Add-on won't start**: Check the logs for dependency issues or configuration errors
2. **No messages received**: Verify your Nostr keys and relay URL are correct
3. **Webhook not triggering**: Ensure the webhook URL is correct and accessible

### Checking Logs

1. Navigate to **Supervisor** > **Add-on Store**
2. Click on "HA Nostr Alert"
3. Click on the **Log** tab
4. Look for error messages or warnings

### Configuration Validation

Ensure your configuration follows the correct format:
- Nostr keys should be in the correct npub/nsec format
- Relay URLs should include the protocol (wss:// or ws://)
- Entity lists should be properly formatted YAML arrays

## Next Steps

Once you've verified the add-on is working correctly:
1. Test with real Home Assistant entities
2. Fine-tune the configuration for your specific use case
3. Monitor reliability and performance
4. Consider contributing improvements back to the project

## Security Considerations

- Keep your private key secure and never share it
- Use secure relay connections (wss://) when possible
- Regularly review and rotate your Nostr keys
- Monitor the add-on logs for any unusual activity
