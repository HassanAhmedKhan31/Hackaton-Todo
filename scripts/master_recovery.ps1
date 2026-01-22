Write-Host "Cleaning up existing deployment..."
helm uninstall hackathon-todo
kubectl delete pods --all --wait=false

Write-Host "Connecting to Minikube Docker..."
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

Write-Host "Building images..."
docker build -t hackathon-todo-backend:latest backend/
docker build -t hackathon-todo-frontend:latest frontend/
docker build -t notification-service:latest backend/notification_service/
docker build -t recurring-service:latest backend/recurring_service/

Write-Host "Re-deploying with Local Images..."
helm install hackathon-todo k8s/hackathon-todo --set secrets.databaseUrl="postgresql://neondb_owner:npg_6sP4OukMImzy@ep-fragrant-glitter-a5214088-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

Write-Host "Deployment Complete. Run 'kubectl get pods -w' to watch startup."