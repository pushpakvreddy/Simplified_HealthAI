# Docker Setup & Deployment Guide

This guide provides instructions to run the **Unified Health AI Platform** using Docker and Docker Desktop.

## 🐳 Prerequisites
1. **Docker Desktop**: Install from [docker.com](https://www.docker.com/products/docker-desktop/).
2. Ensure Docker is running in your system tray.

## 🚀 One-Command Launch
To build and start the entire platform (Frontend, Backend, and MLflow), run:

```bash
docker-compose up --build
```

## 🌐 Accessing Services
Once the containers are healthy:
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **MLflow UI**: [http://localhost:5001](http://localhost:5001)

## 🛠️ Build & Run Commands

### 1. Build and start in background
```bash
docker-compose up -d --build
```

### 2. Stop all services
```bash
docker-compose down
```

### 3. View Logs
```bash
docker-compose logs -f
```

## 🔍 Troubleshooting

### Port 3000/8000/5000 is busy
Ensure you don't have local instances of the backend (uvicorn) or frontend (npm) running. Stop them before running docker-compose.

### Changes not reflecting
If you modify the source code, rebuild the containers:
```bash
docker-compose up --build
```

### MLflow data missing
The `mlruns` directory is mapped as a volume. If you delete the folder on your host machine, the experiments will be cleared.
