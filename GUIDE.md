# Claude Browser API Server for OpenHands - User Guide

This guide will help you set up and use the Claude Browser API server with OpenHands.

## Getting Started

1. The server is already running on:
   - API Server: http://localhost:54402
   - Test Page: http://localhost:58943/test.html

2. You can test the API directly using the test page at http://localhost:58943/test.html

## Configuring OpenHands to Use Claude

1. Open OpenHands in your browser

2. Go to Settings > LLM Providers

3. Add a new Custom LLM with the following settings:
   - Name: Claude Browser
   - API URL: http://localhost:54402/v1/chat/completions
   - Model: claude-3-opus (or any name you prefer)
   - API Key: (leave empty or enter any value)

4. Save the settings

5. Select Claude Browser as your LLM provider

## How It Works

The server uses browser automation to:
1. Log into your Claude.ai account
2. Create a new chat for each request
3. Send your message (including any system prompt)
4. Wait for Claude to respond
5. Return the response to OpenHands

## Demo Mode vs. Real Mode

### Currently Running in Demo Mode
The server is currently running in demo mode, which means:
- No actual browser automation is occurring
- The server returns mock responses
- This is perfect for testing the integration with OpenHands

### Switching to Real Mode
To use your actual Claude.ai account:

1. Stop the server by finding its process ID and killing it:
   ```
   ps aux | grep python
   kill <PID>
   ```

2. Delete the config file:
   ```
   rm /workspace/claude_browser_server/config.json
   ```

3. Restart the server:
   ```
   cd /workspace/claude_browser_server
   python run.py
   ```

4. When prompted about demo mode, enter 'n'

5. Enter your Claude.ai email and password

6. Choose whether to run in headless mode (invisible browser) or visible mode

## Troubleshooting

- If you encounter login issues in real mode, try setting `headless` to `false` to see what's happening in the browser.
- The server creates a new chat for each request, so your Claude.ai interface will show multiple chats.
- If the server stops responding, restart it and check the logs for errors.
- If you're just testing the integration with OpenHands, demo mode is sufficient.