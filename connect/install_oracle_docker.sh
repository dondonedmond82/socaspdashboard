#!/bin/bash
set -e

# Variables
ORACLE_PWD="MyPassw0rd"
ORACLE_IMAGE="container-registry.oracle.com/database/enterprise:19.3.0.0"
CONTAINER_NAME="oracle19c"

echo "[1/6] Updating system and installing dependencies..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose

echo "[2/6] Starting Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

echo "[3/6] Logging in to Oracle Container Registry..."
echo "⚠ You must have an Oracle account to pull the image."
echo "Register here: https://container-registry.oracle.com"
echo "Then sign in below..."
docker login container-registry.oracle.com

echo "[4/6] Pulling Oracle Database 19c image..."
docker pull $ORACLE_IMAGE

echo "[5/6] Running Oracle Database 19c container..."
docker run -d --name $CONTAINER_NAME \
    -p 1521:1521 -p 5500:5500 \
    -e ORACLE_PWD=$ORACLE_PWD \
    -e ORACLE_SID=ORCLCDB \
    -e ORACLE_PDB=ORCLPDB1 \
    $ORACLE_IMAGE

echo "[6/6] Installation complete!"
echo "======================================="
echo "Oracle Database 19c is running in Docker"
echo "Connect with:"
echo "  Host: localhost"
echo "  Port: 1521"
echo "  SID: ORCLCDB"
echo "  PDB: ORCLPDB1"
echo "  User: sys / $ORACLE_PWD (as sysdba)"
echo "Web Console: https://localhost:5500/em"
echo "======================================="
