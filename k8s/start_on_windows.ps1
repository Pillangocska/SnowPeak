# setup.ps1

Write-Host "🚀 Starting Snow Peak application setup..." -ForegroundColor Cyan

# Function to check if a command exists
function Test-CommandExists {
    param ($command)
    $exists = Get-Command -Name $command -ErrorAction SilentlyContinue
    return ($null -ne $exists)
}

# Check prerequisites
Write-Host "✨ Checking prerequisites..." -ForegroundColor Yellow
if (-not (Test-CommandExists "kubectl")) {
    Write-Host "❌ kubectl not found. Please install kubectl first." -ForegroundColor Red
    exit 1
}
if (-not (Test-CommandExists "minikube")) {
    Write-Host "❌ minikube not found. Please install minikube first." -ForegroundColor Red
    exit 1
}

# Check if minikube is running
$minikubeStatus = minikube status --format '{{.Host}}' 2>&1
if ($minikubeStatus -ne "Running") {
    Write-Host "🔄 Starting Minikube..." -ForegroundColor Yellow
    minikube start
}

# Create ConfigMaps
Write-Host "📦 Creating ConfigMaps..." -ForegroundColor Yellow

# Delete existing ConfigMaps to ensure clean state
kubectl delete configmap keycloak-realms-config --ignore-not-found
kubectl delete configmap rabbitmq-plugins-config --ignore-not-found
kubectl delete configmap nginx-config --ignore-not-found

# Create new ConfigMaps with updated paths
kubectl create configmap keycloak-realms-config --from-file=./keycloak/realms/
kubectl create configmap rabbitmq-plugins-config --from-file=enabled_plugins=./rabbitmq_enabled_plugins
kubectl create configmap nginx-config --from-file=nginx.conf=./client/nginx.conf

# Apply Kubernetes manifests from k8s folder
Write-Host "🎮 Applying Kubernetes manifests..." -ForegroundColor Yellow
kubectl apply -f ./k8s/manifest_prod.yaml

# Wait for pods to be ready
Write-Host "⏳ Waiting for pods to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10  # Give some time for pods to start

# Function to check if a pod is ready
function Wait-ForPod {
    param ($podPrefix)

    Write-Host "Waiting for $podPrefix..." -ForegroundColor Gray
    $ready = $false
    $attempts = 0
    $maxAttempts = 20

    while (-not $ready -and $attempts -lt $maxAttempts) {
        $pod = kubectl get pods | Select-String "^$podPrefix"
        if ($pod -match "Running") {
            $ready = $true
            Write-Host "✅ $podPrefix is ready" -ForegroundColor Green
        } else {
            $attempts++
            Write-Host "Waiting for $podPrefix... Attempt $attempts of $maxAttempts" -ForegroundColor Gray
            Start-Sleep -Seconds 2
        }
    }

    if (-not $ready) {
        Write-Host "❌ Timeout waiting for $podPrefix" -ForegroundColor Red
    }
}

# Wait for critical services
Wait-ForPod "rabbitmq"
Wait-ForPod "backend"
#Wait-ForPod "frontend"


# Setup port forwarding
Write-Host "🔌 Setting up port forwarding..." -ForegroundColor Yellow

# Function to start port forwarding
function Start-PortForward {
    param ($service, $localPort, $servicePort)
    $job = Start-Process -NoNewWindow powershell -ArgumentList "kubectl port-forward service/$service $localPort`:$servicePort"
    return $job
}

# Start port forwarding for services
Start-PortForward "rabbitmq" "15672" "15672"  # RabbitMQ Management
Start-PortForward "rabbitmq" "15674" "15674"  # RabbitMQ WebSocket
Start-PortForward "frontend" "4200" "4200"    # Frontend
Start-PortForward "keycloak" "9090" "8080"    # Keycloak

Write-Host "✅ Setup completed! Services are available at:" -ForegroundColor Green
Write-Host "📊 RabbitMQ Management: http://localhost:15672" -ForegroundColor Cyan
Write-Host "🌐 Frontend: http://localhost:4200" -ForegroundColor Cyan
Write-Host "🔒 Keycloak: http://localhost:9090" -ForegroundColor Cyan
Write-Host "⚠️ Keep this window open to maintain port forwarding" -ForegroundColor Yellow
