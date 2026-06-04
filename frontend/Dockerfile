# Frontend Dockerfile — multi-stage build
# Build context MUST be the project root so nginx.conf is accessible

# Stage 1: Build the Vue app
FROM node:20-alpine AS builder

WORKDIR /app

COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN npm install

COPY frontend/. .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config from project root
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy favicon if exists (ignore if missing)
COPY --from=builder /app/dist/favicon.ico /usr/share/nginx/html/favicon.ico

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
