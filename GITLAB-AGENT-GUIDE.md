# GitLab Agent Setup Guide

## Current Status
  ✅ Agent registered in GitLab: gitdeeper3-k8s
  ✅ Configuration file created
  ❌ Not connected to Kubernetes

## To Complete Setup:

### Step 1: Get Kubernetes Cluster
Options:
- Local: Minikube, Kind, Docker Desktop
- Cloud: Google GKE, AWS EKS, Azure AKS (free tiers available)
- Remote: Any Kubernetes cluster

### Step 2: Install Helm
```bash
# On Linux/Mac
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Or via package manager
# Ubuntu/Debian: sudo apt install helm
# Mac: brew install helm
```

Step 3: Deploy GitLab Agent

```bash
# Get agent token from GitLab UI
# Then run:
helm upgrade --install gitdeeper3-k8s gitlab/gitlab-agent \
    --namespace gitlab-agent-gitdeeper3-k8s \
    --create-namespace \
    --set config.token=YOUR_AGENT_TOKEN \
    --set config.kasAddress=wss://kas.gitlab.com
```

Step 4: Verify Connection

1. Wait 1-2 minutes
2. Check GitLab: Infrastructure → Kubernetes
3. Status should change to "Connected"

Managed from Termux

This configuration was managed from Termux on Android.
Last updated: $(date)
