#!/bin/bash

# Check if email is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <email> [headless]"
    echo "  email: Your Claude.ai email address"
    echo "  headless: true or false (default: false)"
    echo ""
    echo "NOTE: You will need to complete the authentication manually in the browser."
    echo "      It's recommended to use headless=false to see the browser window."
    exit 1
fi

EMAIL=$1
HEADLESS=${2:-false}

# Create a real mode config.json
cat > config.json << EOL
{
  "email": "$EMAIL",
  "auth_method": "manual",
  "headless": $HEADLESS,
  "demo_mode": false
}
EOL

# Start the server with Docker Compose
docker-compose up -d

echo "Claude Browser Server started in real mode!"
echo "Using email: $EMAIL"
echo "Headless mode: $HEADLESS"
echo "Authentication method: manual"
echo ""
echo "IMPORTANT: If headless=false, you should see a browser window open."
echo "           You'll need to complete the authentication process manually."
echo "           This may involve checking your email for a verification code"
echo "           or using a third-party login option like Google."
echo ""
echo "You can access the API at: http://localhost:54402/v1/chat/completions"
echo "To view logs: docker-compose logs -f"
echo "To stop the server: docker-compose down"