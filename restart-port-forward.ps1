# PowerShell Script to Restart Kubectl Port-Forwarding

# --- CONFIGURATION ---
$frontendPort = 3000
$backendPort = 8000
$frontendService = "hackathon-todo-frontend"
$backendService = "hackathon-todo-backend"

# --- FUNCTION TO KILL PROCESS BY PORT ---
function Stop-ProcessByPort {
    param (
        [int]$port
    )
    try {
        $processId = (Get-NetTCPConnection -LocalPort $port -State Listen).OwningProcess
        if ($processId) {
            $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
            if ($process) {
                Write-Host "Stopping process $($process.Name) (PID: $($process.Id)) on port $port"
                Stop-Process -Id $process.Id -Force
            }
        } else {
            Write-Host "No process found listening on port $port."
        }
    } catch {
        Write-Warning "Could not stop process on port $port. It might not be running or you may need elevated permissions."
    }
}

# --- RESTART PORT-FORWARDING ---
Write-Host "--- Restarting Port-Forwarding for Frontend and Backend ---"

# 1. Stop existing port-forwards
Stop-ProcessByPort -port $frontendPort
Stop-ProcessByPort -port $backendPort

# Give a moment for ports to be released
Start-Sleep -Seconds 2

# 2. Start new port-forwards in the background
Write-Host "Starting port-forward for $frontendService on port $frontendPort..."
Start-Process -NoNewWindow -FilePath "kubectl" -ArgumentList "port-forward service/$frontendService ${frontendPort}:3000"

Write-Host "Starting port-forward for $backendService on port $backendPort..."
Start-Process -NoNewWindow -FilePath "kubectl" -ArgumentList "port-forward service/$backendService ${backendPort}:8000"

Write-Host "--- Port-forwarding has been restarted in the background. ---"
