# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm install

# Copy rest of the application
COPY . .

# Build the application
RUN npm run build

# Add debug ls to see what's in the output directory
RUN ls -la /app/dist/snow-peak-client/browser

# Stage 2: Run
FROM nginx:1.25-alpine

# Remove default nginx configuration
RUN rm -rf /etc/nginx/conf.d/default.conf
RUN rm -rf /etc/nginx/nginx.conf
RUN rm -rf /usr/share/nginx/html/*

# Copy custom configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create directory for your app
RUN mkdir -p /usr/share/nginx/html

# Copy built assets
COPY --from=builder /app/dist/snow-peak-client/browser/ /usr/share/nginx/html/

# Debug: List contents of nginx html directory
RUN ls -la /usr/share/nginx/html

EXPOSE 80

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget -q --no-cache --spider http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
