# Guide: Resolving Minikube Connectivity and RBAC Errors

This guide provides a complete walkthrough to reset your Minikube environment, load local Docker images, and fix common networking issues on Windows 10.

## 1. Hard Reset Minikube to Fix RBAC and Initialization Errors

RBAC (Role-Based Access Control) errors, like the one you're seeing with `system:kube-controller-manager`, often point to a corrupted or misconfigured Minikube cluster. The most effective solution is a "hard reset."

Follow these steps in your terminal:

### Step 1: Delete the Existing Cluster

This command will remove the Minikube VM and all its associated resources.

```bash
minikube delete
```

### Step 2: (Optional but Recommended) Purge All Local Minikube Data

To ensure a completely fresh start, you can remove the `.minikube` directory from your user profile. This directory contains cached images and configurations that might persist across resets.

**Warning:** This will remove all profiles and cached data.

Open PowerShell and run:

```powershell
rm -r ~/.minikube
```

### Step 3: Start Minikube Anew

Now, start a new cluster. This will download the necessary components and re-initialize the control plane, including RBAC permissions.

```bash
minikube start
```

After this, your cluster should be running in a clean state, which should resolve the RBAC forbidden errors.

---

## 2. Load Local Images to Bypass Internet Registries

Since you're having trouble pulling from `registry.k8s.io`, you can build your images locally and load them directly into Minikube's internal Docker daemon. This makes your deployment independent of an internet connection.

### Step 1: Build Your Docker Images

First, ensure your `backend` and `frontend` images are built and tagged. From your project's root directory, run:

```bash
docker build -t hackathon-backend:latest ./backend
docker build -t hackathon-frontend:latest ./frontend
```

### Step 2: Load Images into Minikube

Use the `minikube image load` command to push the images from your local Docker Desktop into the Minikube cluster:

```bash
minikube image load hackathon-backend:latest
minikube image load hackathon-frontend:latest
```

Minikube will confirm that the image has been loaded. Now, your Kubernetes cluster can find these images locally.

---

## 3. Configure `imagePullPolicy` to Use Local Images

To ensure Kubernetes uses the local images you just loaded and *never* tries to pull them from a remote registry, you need to set the `imagePullPolicy` to `Never` or `IfNotPresent`.

Your Helm chart is already correctly configured for this.

-   **File:** `k8s/hackathon-todo/values.yaml`
-   **Configuration:**

```yaml
backend:
  image:
    repository: hackathon-backend
    pullPolicy: Never # <-- This tells Kubernetes not to pull the image

frontend:
  image:
    repository: hackathon-frontend
    pullPolicy: Never # <-- This tells Kubernetes not to pull the image
```

Because your `values.yaml` specifies `pullPolicy: Never`, your Helm deployments for the `backend` and `frontend` will use the images you loaded in the previous step. No changes are needed here, but it's important to understand *why* it works.

---

## 4. Fix Docker Desktop `TLS handshake timeout` on Windows 10

A `TLS handshake timeout` error when pulling images is almost always a networking issue between your host machine and the Docker/Minikube VM. Here are the most common causes and their solutions on Windows 10.

### Cause 1: Corporate Proxy

If you are on a corporate network, a proxy may be intercepting traffic.

-   **Fix:** Configure Docker Desktop to use your company's proxy.
    1.  Go to **Docker Desktop > Settings > Resources > Proxies**.
    2.  Enter your proxy details.
    3.  Apply & Restart.

### Cause 2: MTU Size Mismatch

The MTU (Maximum Transmission Unit) size of your host's network adapter might differ from the Docker VM's, causing packet fragmentation and timeouts.

-   **Fix:** Adjust the MTU in Docker's configuration.

    1.  **Find your host's MTU:** Open PowerShell and run `netsh interface ipv4 show subinterfaces`. Look for the MTU of your primary network adapter (e.g., "Wi-Fi" or "Ethernet"). It's usually `1500`.

    2.  **Set Docker's MTU:**
        -   Go to **Docker Desktop > Settings > Docker Engine**.
        -   Add the `mtu` key to the JSON configuration. If your host MTU was 1500, a value of `1460` is a safe starting point.

        ```json
        {
          "builder": {
            "gc": {
              "defaultKeepStorage": "20GB",
              "enabled": true
            }
          },
          "experimental": false,
          "mtu": 1460
        }
        ```

    3.  Apply & Restart Docker.

### Cause 3: Windows Firewall or Antivirus

Your firewall or antivirus software might be blocking traffic from the Minikube or Docker VM.

-   **Fix:** Add firewall exceptions for Docker and Minikube.
    -   Temporarily disable your firewall to see if the issue is resolved.
    -   If it is, create inbound and outbound rules to allow traffic for `Docker Desktop.exe` and `minikube.exe`.

By following these steps, you should have a clean, functional Minikube environment that can deploy your local application without requiring a connection to external image registries.
