#!/bin/bash

# Check if email and password are provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <email> <password> [headless]"
    echo "  email: Your Claude.ai email address"
    echo "  password: Your Claude.ai password"
    echo "  headless: true or false (default: true)"
    exit 1
fi

EMAIL=$1
PASSWORD=$2
HEADLESS=${3:-true}

# Create a real mode config.json
cat > config.json << EOL
{
  "email": "$EMAIL",
  "password": "$PASSWORD",
  "headless": $HEADLESS,
  "demo_mode": false
}
EOL

# Start the server with Docker Compose
docker-compose up -d

echo "Claude Browser Server started in real mode!"
echo "Using email: $EMAIL"
echo "Headless mode: $HEADLESS"
echo "You can access the API at: http://localhost:54402/v1/chat/completions"
echo "To view logs: docker-compose logs -f"
echo "To stop the server: docker-compose down"