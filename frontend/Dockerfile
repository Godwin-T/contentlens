# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration (ensure you have the correct nginx.conf)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 as that's the default for Nginx
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
