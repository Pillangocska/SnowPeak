# Stage 1: Build the Angular application
FROM node:20-alpine as builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve the application
FROM nginx:1.25-alpine

COPY nginx.conf /data/conf/nginx.conf

# Copy the built application from builder stage
COPY --from=builder /app/dist/snow-peak-client /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-c", "/data/conf/nginx.conf", "-g", "daemon off;"]