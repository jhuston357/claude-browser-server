#!/bin/bash

# This script helps users enter a verification code into a running Docker container

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <verification_code>"
    echo "  verification_code: The code you received in your email"
    echo ""
    echo "Example:"
    echo "  $0 123456"
    exit 1
fi

VERIFICATION_CODE=$1

# Get the container ID
CONTAINER_ID=$(docker-compose ps -q claude-browser-server)

if [ -z "$CONTAINER_ID" ]; then
    echo "Error: Claude Browser Server container is not running."
    echo "Start it first with: ./start-real-mode.sh your-email@example.com"
    exit 1
fi

echo "Sending verification code: $VERIFICATION_CODE"
echo "$VERIFICATION_CODE" | docker exec -i $CONTAINER_ID bash -c 'cat > /tmp/verification_code.txt'

echo "Verification code sent to container."
echo "If the prompt is still waiting for input, you may need to restart the server."
echo "Check the logs with: docker-compose logs -f"