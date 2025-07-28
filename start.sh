#!/bin/sh

# Start Python backend
cd /app/backend
python3 server.py &

# Start nginx
nginx -g "daemon off;" 