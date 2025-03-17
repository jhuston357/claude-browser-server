# Claude Browser API Server for OpenHands - User Guide

This guide will help you set up and use the Claude Browser API server with OpenHands.

## Getting Started

### Option 1: Running the Pre-built Server
If someone has already set up the server for you:

1. The server should be running on:
   - API Server: http://localhost:54402
   - Test Page: http://localhost:58943/test.html

2. You can test the API directly using the test page at http://localhost:58943/test.html

### Option 2: Running Locally
To run the server locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. Run the server:
   ```bash
   python run.py
   ```

3. Follow the prompts to configure the server

### Option 3: Running with Docker (Recommended)
The easiest way to deploy is using Docker:

1. For demo mode (no real Claude access):
   ```bash
   ./start-demo.sh
   ```

2. For real mode with your Claude.ai account:
   ```bash
   ./start-real-mode.sh your-email@example.com your-password
   ```
   
   To run with a visible browser (for debugging):
   ```bash
   ./start-real-mode.sh your-email@example.com your-password false
   ```

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

### Demo Mode
In demo mode:
- No actual browser automation occurs
- The server returns mock responses
- This is perfect for testing the integration with OpenHands

### Real Mode
In real mode:
- The server logs into your Claude.ai account
- It creates a new chat for each request
- It sends your message and waits for Claude to respond
- It returns the actual response from Claude

## Switching Between Modes

### Using Docker (Recommended)
1. Stop the current container:
   ```bash
   docker-compose down
   ```

2. Delete the config file:
   ```bash
   rm config.json
   ```

3. Start in your desired mode:
   ```bash
   # For demo mode
   ./start-demo.sh
   
   # For real mode
   ./start-real-mode.sh your-email@example.com your-password
   ```

### Running Locally
1. Stop the server by finding its process ID and killing it:
   ```bash
   ps aux | grep python
   kill <PID>
   ```

2. Delete the config file:
   ```bash
   rm config.json
   ```

3. Restart the server:
   ```bash
   python run.py
   ```

4. Follow the prompts to configure your desired mode

## Troubleshooting

- If you encounter login issues in real mode, try setting `headless` to `false` to see what's happening in the browser.
- The server creates a new chat for each request, so your Claude.ai interface will show multiple chats.
- If the server stops responding, restart it and check the logs for errors.
- If you're just testing the integration with OpenHands, demo mode is sufficient.
- For Docker issues, check the logs with `docker-compose logs -f`