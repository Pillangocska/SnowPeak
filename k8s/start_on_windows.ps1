Write-Host "🚀 Starting Snow Peak application setup..." -ForegroundColor Cyan

# Check prerequisites
if (-not (Get-Command "kubectl" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ kubectl not found" -ForegroundColor Red
    exit 1
}
if (-not (Get-Command "minikube" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ minikube not found" -ForegroundColor Red
    exit 1
}

# Start minikube if not running
if ((minikube status --format '{{.Host}}' 2>&1) -ne "Running") {
    Write-Host "🔄 Starting Minikube..." -ForegroundColor Yellow
    minikube start
}

# Create ConfigMaps
Write-Host "📦 Creating ConfigMaps..." -ForegroundColor Yellow
kubectl delete configmap keycloak-realms-config --ignore-not-found
kubectl delete configmap rabbitmq-plugins-config --ignore-not-found
kubectl delete configmap nginx-config --ignore-not-found

kubectl create configmap keycloak-realms-config --from-file=./keycloak/realms/
kubectl create configmap rabbitmq-plugins-config --from-file=enabled_plugins=./rabbitmq_enabled_plugins
kubectl create configmap nginx-config --from-file=nginx.conf=./client/nginx.conf

# Apply Kubernetes manifests
Write-Host "🎮 Applying Kubernetes manifests..." -ForegroundColor Yellow
kubectl apply -f ./k8s/manifest_prod.yaml

# Wait for pods
function Wait-ForPod {
    param ($podPrefix)
    Write-Host "Waiting for $podPrefix..." -ForegroundColor Gray
    $attempts = 0
    while ($attempts -lt 20) {
        if ((kubectl get pods | Select-String "^$podPrefix") -match "Running") {
            Write-Host "✅ $podPrefix is ready" -ForegroundColor Green
            return
        }
        $attempts++
        Start-Sleep -Seconds 2
    }
    Write-Host "❌ Timeout waiting for $podPrefix" -ForegroundColor Red
}

# Wait for critical services
@("db", "keycloak-postgres", "keycloak", "rabbitmq", "ski-lift-1",
  "ski-lift-2", "ski-lift-3", "backend", "frontend") | ForEach-Object {
    Wait-ForPod $_
}

# Start minikube tunnel
Write-Host "🚇 Starting minikube tunnel..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "minikube tunnel" -NoNewWindow

Write-Host "✅ Setup completed! Services are available at:" -ForegroundColor Green
Write-Host "📊 RabbitMQ Management: http://localhost:15672" -ForegroundColor Cyan
Write-Host "🌐 Frontend: http://localhost:80" -ForegroundColor Cyan
Write-Host "🔒 Keycloak: http://localhost:9090" -ForegroundColor Cyan
Write-Host "⚠️ Keep this window open to maintain tunnel connection" -ForegroundColor Yellow
