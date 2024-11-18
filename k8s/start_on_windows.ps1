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
Wait-ForPod "db"
Wait-ForPod "keycloak-postgres"
Wait-ForPod "keycloak"
Wait-ForPod "rabbitmq"
Wait-ForPod "ski-lift-1"
Wait-ForPod "ski-lift-2"
Wait-ForPod "ski-lift-3"
Wait-ForPod "backend"
Wait-ForPod "frontend"

# Function to check if port is in use
function Test-PortInUse {
    param($port)
    $inUse = $false
    $listener = $null

    try {
        $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Loopback, $port)
        $listener.Start()
        $inUse = $false
    }
    catch {
        $inUse = $true
    }
    finally {
        if ($listener -ne $null) {
            $listener.Stop()
        }
    }

    return $inUse
}

# Function to kill process using a port
function Stop-ProcessOnPort {
    param($port)
    $processInfo = netstat -ano | findstr ":$port"
    if ($processInfo) {
        $processId = ($processInfo -split '\s+')[-1]
        try {
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped process using port $port (PID: $processId)" -ForegroundColor Yellow
            Start-Sleep -Seconds 1
        }
        catch {
            Write-Host "Failed to stop process on port $port" -ForegroundColor Red
        }
    }
}

# Simplified function to start port forwarding
function Start-PortForward {
    param ($service, $localPort, $servicePort)

    # Check if port is in use
    if (Test-PortInUse $localPort) {
        Write-Host "Port $localPort is in use. Attempting to free it..." -ForegroundColor Yellow
        Stop-ProcessOnPort $localPort
    }

    # Try to start port forwarding
    try {
        $job = Start-Process -NoNewWindow powershell -ArgumentList "kubectl port-forward service/$service $localPort`:$servicePort" -PassThru
        Write-Host "Started port forwarding for $service on port $localPort" -ForegroundColor Green
        # Give it a moment to establish
        Start-Sleep -Seconds 2
        return $job
    }
    catch {
        Write-Host "Failed to start port forwarding for $service on port $localPort" -ForegroundColor Red
        Write-Host $_.Exception.Message
        return $null
    }
}

# Setup port forwarding
Write-Host "🔌 Setting up port forwarding..." -ForegroundColor Yellow

# Store port forwarding jobs
$portForwardJobs = @()

# Start port forwarding for services
# servicePort is the service's external port and localport is what we will access
$services = @(
    @{service="rabbitmq"; localPort=15672; servicePort=15672},
    @{service="frontend"; localPort=80; servicePort=80},
    @{service="keycloak"; localPort=9090; servicePort=9090}
)

foreach ($svc in $services) {
    $job = Start-PortForward -service $svc.service -localPort $svc.localPort -servicePort $svc.servicePort
    if ($job) {
        $portForwardJobs += $job
        # Add small delay between services
        Start-Sleep -Seconds 10
    }
}

# Display status
if ($portForwardJobs.Count -eq $services.Count) {
    Write-Host "✅ Setup completed! Services are available at:" -ForegroundColor Green
    Write-Host "📊 RabbitMQ Management: http://localhost:15672" -ForegroundColor Cyan
    Write-Host "🌐 Frontend: http://localhost:80" -ForegroundColor Cyan
    Write-Host "🔒 Keycloak: http://localhost:9090" -ForegroundColor Cyan
    Write-Host "⚠️ Keep this window open to maintain port forwarding" -ForegroundColor Yellow
} else {
    Write-Host "⚠️ Not all services were successfully forwarded" -ForegroundColor Yellow
}

# Add cleanup on script exit
$exitScript = {
    Write-Host "Cleaning up port forwarding processes..." -ForegroundColor Yellow
    foreach ($job in $portForwardJobs) {
        if ($job.HasExited -eq $false) {
            Stop-Process -Id $job.Id -Force
        }
    }
}

# Register the cleanup script
Register-EngineEvent PowerShell.Exiting -Action $exitScript | Out-Null
