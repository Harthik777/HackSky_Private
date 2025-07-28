# Multi-stage build for React frontend and Python backend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.11-slim AS backend

WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

FROM nginx:alpine AS production

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Copy backend
COPY --from=backend /app/backend /app/backend

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Install Python in nginx container
RUN apk add --no-cache python3 py3-pip
RUN pip3 install -r /app/backend/requirements.txt

EXPOSE 80 5000

# Start both nginx and Python backend
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"] 