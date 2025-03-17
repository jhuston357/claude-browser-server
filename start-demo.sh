#!/bin/bash

# Create a demo mode config.json
cat > config.json << EOL
{
  "email": "demo@example.com",
  "password": "demo_password",
  "headless": true,
  "demo_mode": true
}
EOL

# Start the server with Docker Compose
docker-compose up -d

echo "Claude Browser Server started in demo mode!"
echo "You can access the API at: http://localhost:54402/v1/chat/completions"
echo "To view logs: docker-compose logs -f"
echo "To stop the server: docker-compose down"