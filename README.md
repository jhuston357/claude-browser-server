# Claude Browser API Server for OpenHands

This server allows OpenHands to use Anthropic's Claude through the browser interface at claude.ai, without requiring an API key.

## Features

- Logs into your Claude.ai account through the browser
- Sends messages to Claude and retrieves responses
- Exposes an API endpoint compatible with OpenHands
- Supports system prompts
- Includes a demo mode for testing without credentials
- Docker support for easy deployment

## Getting Started

### Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. Run the server:
   ```bash
   python run.py
   ```

3. On first run, you'll be prompted to choose between demo mode or real mode:
   
   **Demo Mode:**
   - Select 'y' when asked about demo mode
   - No actual browser automation will occur
   - The server will return mock responses
   
   **Real Mode:**
   - Enter your Claude.ai email address
   - The authentication is manual - you'll need to:
     - Complete the verification process in the browser window
     - This may involve checking your email for a verification code
     - Or using a third-party login option like Google
   - It's recommended to run with a visible browser (not headless) for authentication

### Running with Docker

1. For demo mode (no real Claude access):
   ```bash
   ./start-demo.sh
   ```

2. For real mode with your Claude.ai account:

   **Option A: Verification Code Authentication (best for SSH/headless servers)**
   ```bash
   ./start-real-mode.sh your-email@example.com
   ```
   
   This will run in headless mode and prompt you to enter the verification code in the terminal.
   
   **Option B: Manual Authentication (requires visible browser)**
   ```bash
   ./start-real-mode.sh your-email@example.com manual
   ```
   
   This will start the server with a visible browser window so you can complete the authentication process.

3. Check the logs to see the server status:
   ```bash
   docker-compose logs -f
   ```

4. If you want to pre-configure before starting Docker, create a `config.json` file in the root directory with the following structure:
   ```json
   {
     "email": "your-email@example.com",
     "auth_method": "manual",
     "headless": false,
     "demo_mode": false
   }
   ```
   
   For demo mode:
   ```json
   {
     "email": "demo@example.com",
     "auth_method": "manual",
     "headless": true,
     "demo_mode": true
   }
   ```
   
   **Note about authentication**: Claude.ai uses email verification or third-party login (like Google) rather than passwords. There are two authentication methods available:
   
   - `verification_code`: You'll be prompted to enter the verification code in the terminal. This is ideal for SSH connections or headless servers.
   - `manual`: You'll need to complete the authentication process in the browser window. For this method, it's recommended to set `headless` to `false` so you can see the browser window.

## Connecting to OpenHands

In OpenHands, add a custom LLM with the following settings:
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
- For Docker issues, make sure the container has the necessary permissions to run browser automation.