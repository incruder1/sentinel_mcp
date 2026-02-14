#!/bin/bash
# Archestra Local Setup Script
# Time-boxed: 2 hours max for Option A attempt

set -e

echo "🚀 Starting Archestra Local Deployment"
echo "========================================"
echo ""

# Check Docker is running
if ! docker ps >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Pull Archestra image
echo "📦 Pulling Archestra platform image..."
docker pull archestra/platform:latest

# Stop any existing Archestra containers
echo "🧹 Cleaning up existing containers..."
docker stop archestra 2>/dev/null || true
docker rm archestra 2>/dev/null || true

# Run Archestra
echo "🏃 Starting Archestra container..."
docker run -d \
  --name archestra \
  -p 9000:9000 \
  -p 3000:3000 \
  -e ARCHESTRA_QUICKSTART=true \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v archestra-postgres-data:/var/lib/postgresql/data \
  -v archestra-app-data:/app/data \
  archestra/platform:latest

echo ""
echo "⏳ Waiting for Archestra to start (this may take 1-2 minutes)..."
sleep 30

# Check if services are up
echo "🔍 Checking services..."
for i in {1..12}; do
    if curl -s http://localhost:3000 >/dev/null 2>&1; then
        echo "✅ Admin UI is ready at http://localhost:3000"
        break
    fi
    if [ $i -eq 12 ]; then
        echo "⚠️  Admin UI not responding yet. Check logs with: docker logs archestra"
    fi
    sleep 5
done

for i in {1..12}; do
    if curl -s http://localhost:9000/health >/dev/null 2>&1; then
        echo "✅ API is ready at http://localhost:9000"
        break
    fi
    if [ $i -eq 12 ]; then
        echo "⚠️  API not responding yet. Check logs with: docker logs archestra"
    fi
    sleep 5
done

echo ""
echo "🎉 Archestra is running!"
echo ""
echo "Next steps:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Check API: curl http://localhost:9000/health"
echo "3. View logs: docker logs archestra -f"
echo ""
echo "To stop: docker stop archestra"
echo "To remove: docker rm archestra"
