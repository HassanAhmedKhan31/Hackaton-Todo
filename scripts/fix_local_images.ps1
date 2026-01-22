# Task ID: T-Fix-Images
# Automation Script to Sync Local Images with Minikube

Write-Host "🔄 Connecting to Minikube Docker Environment..."
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

Write-Host "🏗️ Rebuilding Images INSIDE Minikube..."
docker build -t hackathon-backend:latest backend/
docker build -t hackathon-frontend:latest frontend/
docker build -t notification-service:latest backend/notification_service/
docker build -t recurring-service:latest backend/recurring_service/

Write-Host "⚙️ Upgrading Helm Chart (Applying pullPolicy: Never)..."
# Note: We use --install to ensure it works even if not present
# Assuming secrets.databaseUrl is passed or already in a secrets file, 
# but for safety in this script we assume the chart is valid or user will add --set if needed.
# We'll rely on existing values or defaults.
helm upgrade --install hackathon-todo k8s/hackathon-todo

Write-Host "♻️ Restarting Pods to Pick Up New Images..."
kubectl delete pods --all

Write-Host "✅ Done! Run 'kubectl get pods -w' to monitor startup."
