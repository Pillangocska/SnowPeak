#!/bin/bash

# Text colors
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}🚀 Starting Snow Peak application setup...${NC}"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}✨ Checking prerequisites...${NC}"
if ! command_exists kubectl; then
    echo -e "${RED}❌ kubectl not found. Please install kubectl first.${NC}"
    exit 1
fi
if ! command_exists minikube; then
    echo -e "${RED}❌ minikube not found. Please install minikube first.${NC}"
    exit 1
fi

# Check if minikube is running
if ! minikube status | grep -q "host: Running"; then
    echo -e "${YELLOW}🔄 Starting Minikube...${NC}"
    minikube start
fi

# Create ConfigMaps
echo -e "${YELLOW}📦 Creating ConfigMaps...${NC}"

# Delete existing ConfigMaps to ensure clean state
kubectl delete configmap keycloak-realms-config --ignore-not-found
kubectl delete configmap rabbitmq-plugins-config --ignore-not-found
kubectl delete configmap nginx-config --ignore-not-found

# Create new ConfigMaps with updated paths
kubectl create configmap keycloak-realms-config --from-file=./keycloak/realms/
kubectl create configmap rabbitmq-plugins-config --from-file=enabled_plugins=./rabbitmq_enabled_plugins
kubectl create configmap nginx-config --from-file=nginx.conf=./client/nginx.conf

# Apply Kubernetes manifests from k8s folder
echo -e "${YELLOW}🎮 Applying Kubernetes manifests...${NC}"
kubectl apply -f ./k8s/manifest.yaml

# Wait for pods to be ready
echo -e "${YELLOW}⏳ Waiting for pods to be ready...${NC}"
sleep 10  # Give some time for pods to start

# Function to check if a pod is ready
wait_for_pod() {
    local pod_prefix=$1
    echo -e "${GRAY}Waiting for ${pod_prefix}...${NC}"
    local ready=false
    local attempts=0
    local max_attempts=30

    while [ "$ready" = false ] && [ $attempts -lt $max_attempts ]; do
        if kubectl get pods | grep "^${pod_prefix}" | grep -q "Running"; then
            ready=true
            echo -e "${GREEN}✅ ${pod_prefix} is ready${NC}"
        else
            attempts=$((attempts + 1))
            echo -e "${GRAY}Waiting for ${pod_prefix}... Attempt ${attempts} of ${max_attempts}${NC}"
            sleep 2
        fi
    done

    if [ "$ready" = false ]; then
        echo -e "${RED}❌ Timeout waiting for ${pod_prefix}${NC}"
    fi
}

# Wait for critical services
wait_for_pod "rabbitmq"
wait_for_pod "frontend"
wait_for_pod "backend"

# Setup port forwarding
echo -e "${YELLOW}🔌 Setting up port forwarding...${NC}"

# Function to start port forwarding
start_port_forward() {
    local service=$1
    local local_port=$2
    local service_port=$3
    kubectl port-forward "service/${service}" "${local_port}:${service_port}" &
    sleep 2  # Give port forwarding some time to establish
}

# Start port forwarding for services
start_port_forward "rabbitmq" "15672" "15672"  # RabbitMQ Management
start_port_forward "rabbitmq" "15674" "15674"  # RabbitMQ WebSocket
start_port_forward "frontend" "4200" "4200"    # Frontend
start_port_forward "keycloak" "9090" "8080"    # Keycloak

# Store background process PIDs in a file for cleanup
jobs -p > .port-forward.pids

# Trap SIGINT and SIGTERM signals
cleanup() {
    echo -e "${YELLOW}⚠️ Cleaning up port forwarding...${NC}"
    if [ -f .port-forward.pids ]; then
        kill $(cat .port-forward.pids) 2>/dev/null
        rm .port-forward.pids
    fi
    exit 0
}
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}✅ Setup completed! Services are available at:${NC}"
echo -e "${CYAN}📊 RabbitMQ Management: http://localhost:15672${NC}"
echo -e "${CYAN}🌐 Frontend: http://localhost:4200${NC}"
echo -e "${CYAN}🔒 Keycloak: http://localhost:9090${NC}"
echo -e "${YELLOW}⚠️ Press Ctrl+C to stop port forwarding${NC}"

# Keep the script running to maintain port forwarding
while true; do
    sleep 1
done
