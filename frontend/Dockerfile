# Use Node.js 20 alpine (Vite requirement)
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY frontend/ .

# Expose Vite port (mapped to 3000 in docker-compose)
EXPOSE 5173

# Run in development mode with host exposure
CMD ["npm", "run", "dev", "--", "--host"]
