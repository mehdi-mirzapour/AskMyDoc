# AskMyDoc - Azure Deployment Guide

This guide explains how to deploy the AskMyDoc application to Azure Container Instances using the automated GitHub Actions workflow.

## Prerequisites

- Azure account with an active subscription
- GitHub repository with the AskMyDoc code
- Azure CLI installed (for initial setup)

## Azure Resources Setup

### 1. Create Azure Resource Group

```bash
az group create \
  --name askmydoc-rg \
  --location westeurope
```

### 2. Create Azure Container Registry (ACR)

```bash
az acr create \
  --resource-group askmydoc-rg \
  --name askmydocacr \
  --sku Basic \
  --location westeurope
```

### 3. Get ACR Credentials

```bash
# Get the ACR login server
az acr show \
  --name askmydocacr \
  --query loginServer \
  --output tsv

# Enable admin user and get credentials
az acr update --name askmydocacr --admin-enabled true

# Get username
az acr credential show \
  --name askmydocacr \
  --query username \
  --output tsv

# Get password
az acr credential show \
  --name askmydocacr \
  --query "passwords[0].value" \
  --output tsv
```

### 4. Create Azure Service Principal for GitHub Actions

```bash
az ad sp create-for-rbac \
  --name "askmydoc-github-actions" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/askmydoc-rg \
  --sdk-auth
```

**Note**: Replace `{subscription-id}` with your actual Azure subscription ID. Save the entire JSON output - you'll need it for GitHub secrets.

## GitHub Secrets Configuration

Navigate to your GitHub repository → Settings → Secrets and variables → Actions, and add the following secrets:

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `ACR_LOGIN_SERVER` | ACR login server URL | Output from step 3 (e.g., `askmydocacr.azurecr.io`) |
| `ACR_USERNAME` | ACR username | Output from step 3 |
| `ACR_PASSWORD` | ACR password | Output from step 3 |
| `AZURE_CREDENTIALS` | Service principal credentials | Entire JSON output from step 4 |
| `AZURE_RESOURCE_GROUP` | Azure resource group name | `askmydoc-rg` (or your chosen name) |
| `OPENAI_API_KEY` | OpenAI API key | Your OpenAI API key |
| `MISTRAL_API_KEY` | Mistral API key (optional) | Your Mistral API key or leave as `XXXX` |

## Deployment Workflow

### Automatic Deployment

The deployment happens automatically when you push to the `main` branch:

1. **Push code to main branch**:
   ```bash
   git add .
   git commit -m "Deploy to Azure"
   git push origin main
   ```

2. **GitHub Actions will**:
   - Build Docker images for backend, frontend, and nginx
   - Push images to Azure Container Registry
   - Deploy to Azure Container Instances
   - Output the public IP and FQDN

3. **Monitor the deployment**:
   - Go to your GitHub repository → Actions tab
   - Click on the latest workflow run
   - Watch the deployment progress

### Manual Deployment (Optional)

You can also trigger the workflow manually from the GitHub Actions tab.

## Accessing Your Deployed Application

After successful deployment, your application will be available at:

- **HTTP**: `http://askmydoc-app.westeurope.azurecontainer.io`
- **Direct IP**: Check the workflow output or run:
  ```bash
  az container show \
    --resource-group askmydoc-rg \
    --name askmydoc-app \
    --query ipAddress.ip \
    --output tsv
  ```

### Application Endpoints

- **Frontend**: `http://askmydoc-app.westeurope.azurecontainer.io/`
- **Backend API**: `http://askmydoc-app.westeurope.azurecontainer.io/api/`
- **API Docs**: `http://askmydoc-app.westeurope.azurecontainer.io/docs`
- **Health Check**: `http://askmydoc-app.westeurope.azurecontainer.io/health`

## Architecture

The deployment consists of three containers:

1. **Backend** (Port 5882): FastAPI application handling document processing and queries
2. **Frontend** (Port 5881): React application serving the user interface
3. **Nginx** (Port 80): Reverse proxy routing traffic to backend and frontend

```
Internet → Port 80 (Nginx) → {
  /api/* → Backend:5882
  /*     → Frontend:5881
}
```

## Monitoring and Troubleshooting

### View Container Logs

```bash
# View all container logs
az container logs \
  --resource-group askmydoc-rg \
  --name askmydoc-app

# View specific container logs
az container logs \
  --resource-group askmydoc-rg \
  --name askmydoc-app \
  --container-name backend
```

### Check Container Status

```bash
az container show \
  --resource-group askmydoc-rg \
  --name askmydoc-app \
  --query "{Status:instanceView.state,IP:ipAddress.ip,FQDN:ipAddress.fqdn}" \
  --output table
```

### Restart Containers

The GitHub Actions workflow automatically deletes and recreates the container group on each deployment. To manually restart:

```bash
az container restart \
  --resource-group askmydoc-rg \
  --name askmydoc-app
```

### Common Issues

**Issue**: Container fails to start
- **Solution**: Check logs for the specific container using `az container logs`
- Verify environment variables are set correctly in GitHub secrets

**Issue**: Cannot access the application
- **Solution**: Ensure the container group is in "Succeeded" state
- Check that ports 80 and 5882 are exposed in the container group
- Verify DNS name is resolving correctly

**Issue**: API requests fail
- **Solution**: Check nginx configuration is correctly routing `/api/*` to backend
- Verify backend container is healthy using health check endpoint

## Local Testing with Production Images

To test production images locally before deployment:

```bash
# Set environment variables
export ACR_LOGIN_SERVER=askmydocacr.azurecr.io
export OPENAI_API_KEY=your-key-here
export MISTRAL_API_KEY=your-key-here

# Login to ACR
az acr login --name askmydocacr

# Run production compose
docker-compose -f docker-compose.prod.yml up
```

## Cost Optimization

The current configuration uses:
- **Backend**: 1.0 CPU, 1.0 GB RAM
- **Frontend**: 0.5 CPU, 0.5 GB RAM
- **Nginx**: 0.5 CPU, 0.5 GB RAM
- **Total**: 2.0 CPU, 2.0 GB RAM

Estimated cost: ~€50-70/month (depending on region and usage)

To reduce costs:
- Adjust CPU/memory in `azure-container-group.yml`
- Use Azure Container Instances only during business hours
- Consider Azure App Service for production workloads

## Cleanup

To delete all Azure resources:

```bash
# Delete the container group
az container delete \
  --resource-group askmydoc-rg \
  --name askmydoc-app \
  --yes

# Delete the entire resource group (including ACR)
az group delete \
  --name askmydoc-rg \
  --yes
```
