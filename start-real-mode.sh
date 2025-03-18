#!/bin/bash

# Check if email is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <email> [auth_method] [headless]"
    echo "  email: Your Claude.ai email address"
    echo "  auth_method: verification_code or manual (default: verification_code)"
    echo "  headless: true or false (default depends on auth_method)"
    echo ""
    echo "Examples:"
    echo "  $0 your-email@example.com"
    echo "    - Uses verification_code auth (enter code in terminal) with headless=true"
    echo ""
    echo "  $0 your-email@example.com manual"
    echo "    - Uses manual auth (complete in browser) with headless=false"
    echo ""
    echo "  $0 your-email@example.com verification_code false"
    echo "    - Uses verification_code auth with visible browser"
    exit 1
fi

EMAIL=$1
AUTH_METHOD=${2:-verification_code}

# Set default headless value based on auth method
if [ "$AUTH_METHOD" = "verification_code" ]; then
    DEFAULT_HEADLESS=true
else
    DEFAULT_HEADLESS=false
fi

HEADLESS=${3:-$DEFAULT_HEADLESS}

# Create a real mode config.json
cat > config.json << EOL
{
  "email": "$EMAIL",
  "auth_method": "$AUTH_METHOD",
  "headless": $HEADLESS,
  "demo_mode": false
}
EOL

# Start the server with Docker Compose
docker-compose up -d

echo "Claude Browser Server started in real mode!"
echo "Using email: $EMAIL"
echo "Authentication method: $AUTH_METHOD"
echo "Headless mode: $HEADLESS"
echo ""

if [ "$AUTH_METHOD" = "verification_code" ]; then
    echo "IMPORTANT: Watch the logs for a prompt to enter your verification code:"
    echo "  docker-compose logs -f"
    echo ""
    echo "When prompted, enter the verification code sent to your email."
else
    echo "IMPORTANT: If headless=false, you should see a browser window open."
    echo "           You'll need to complete the authentication process manually."
    echo "           This may involve checking your email for a verification code"
    echo "           or using a third-party login option like Google."
fi

echo ""
echo "You can access the API at: http://localhost:54402/v1/chat/completions"
echo "To view logs: docker-compose logs -f"
echo "To stop the server: docker-compose down"