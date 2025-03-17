# Claude Browser API Server for OpenHands

This server allows OpenHands to use Anthropic's Claude through the browser interface at claude.ai, without requiring an API key.

## Features

- Logs into your Claude.ai account through the browser
- Sends messages to Claude and retrieves responses
- Exposes an API endpoint compatible with OpenHands
- Supports system prompts
- Includes a demo mode for testing without credentials

## Getting Started

1. Run the server:
   ```
   cd claude_browser_server
   python run.py
   ```

2. On first run, you'll be prompted to choose between demo mode or real mode:
   
   **Demo Mode:**
   - Select 'y' when asked about demo mode
   - No actual browser automation will occur
   - The server will return mock responses
   
   **Real Mode:**
   - Enter your Claude.ai login credentials:
     - Email
     - Password
     - Whether to run the browser in headless mode (invisible) or visible mode

3. In OpenHands, add a custom LLM with the following settings:
   - Name: Claude Browser
   - API URL: http://localhost:54402/v1/chat/completions
   - Model: claude-3-opus (or any name you prefer)

## How It Works

### Demo Mode
In demo mode, the server simulates Claude's responses without actually connecting to claude.ai. This is useful for testing the integration with OpenHands.

### Real Mode
In real mode, the server uses Playwright to automate a browser that:
1. Logs into your Claude.ai account
2. Creates a new chat for each request
3. Sends your message
4. Waits for Claude to respond
5. Returns the response to OpenHands

## Configuration

Configuration is stored in `config.json` in the root directory. If you need to update your credentials, simply delete this file and restart the server.

## Troubleshooting

- If you encounter login issues, try setting `headless` to `false` to see what's happening in the browser.
- The server creates a new chat for each request, so your Claude.ai interface will show multiple chats.
- If the server stops responding, restart it and check the logs for errors.
- If you're just testing the integration with OpenHands, use demo mode first.