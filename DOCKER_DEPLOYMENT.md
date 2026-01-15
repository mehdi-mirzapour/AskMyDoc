# AskMyDoc - Docker Deployment

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### Local Development

1. **Set environment variables:**
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```

2. **Build and run:**
   ```bash
   docker-compose up --build
   ```

3. **Access the API:**
   - API: http://localhost/
   - API Docs: http://localhost/docs
   - Health Check: http://localhost/health

### Production Deployment (Azure)

#### Option 1: Azure Container Instances (ACI)

1. **Build and push images to Azure Container Registry:**
   ```bash
   # Login to Azure
   az login
   
   # Create resource group
   az group create --name askmydoc-rg --location eastus
   
   # Create container registry
   az acr create --resource-group askmydoc-rg \
     --name askmydocacr --sku Basic
   
   # Login to ACR
   az acr login --name askmydocacr
   
   # Build and push backend
   docker build -t askmydocacr.azurecr.io/backend:latest ./backend
   docker push askmydocacr.azurecr.io/backend:latest
   
   # Build and push nginx
   docker build -t askmydocacr.azurecr.io/nginx:latest ./nginx
   docker push askmydocacr.azurecr.io/nginx:latest
   ```

2. **Deploy to ACI:**
   ```bash
   # Create container group
   az container create \
     --resource-group askmydoc-rg \
     --name askmydoc \
     --image askmydocacr.azurecr.io/nginx:latest \
     --registry-login-server askmydocacr.azurecr.io \
     --registry-username $(az acr credential show --name askmydocacr --query username -o tsv) \
     --registry-password $(az acr credential show --name askmydocacr --query passwords[0].value -o tsv) \
     --dns-name-label askmydoc \
     --ports 80 \
     --environment-variables OPENAI_API_KEY=your-key-here
   ```

#### Option 2: Azure App Service (Container)

1. **Create App Service Plan:**
   ```bash
   az appservice plan create \
     --name askmydoc-plan \
     --resource-group askmydoc-rg \
     --is-linux \
     --sku B1
   ```

2. **Create Web App:**
   ```bash
   az webapp create \
     --resource-group askmydoc-rg \
     --plan askmydoc-plan \
     --name askmydoc-api \
     --deployment-container-image-name askmydocacr.azurecr.io/backend:latest
   ```

3. **Configure environment variables:**
   ```bash
   az webapp config appsettings set \
     --resource-group askmydoc-rg \
     --name askmydoc-api \
     --settings OPENAI_API_KEY=your-key-here
   ```

## Docker Images

### Backend Image
- **Base:** python:3.9-slim
- **Port:** 5888
- **Health Check:** /health endpoint

### Nginx Image
- **Base:** nginx:alpine
- **Port:** 80
- **Configuration:** Reverse proxy to backend

## Environment Variables

### Required
- `OPENAI_API_KEY` - Your OpenAI API key

### Optional
- `MISTRAL_API_KEY` - Mistral API key (if using Mistral model)

## Volumes

- `./backend/uploads` - Persistent storage for uploaded files

## Health Checks

Both containers have health checks configured:
- **Backend:** `http://localhost:5888/health`
- **Nginx:** `http://localhost/health`

## Troubleshooting

### View logs:
```bash
docker-compose logs -f backend
docker-compose logs -f nginx
```

### Rebuild containers:
```bash
docker-compose down
docker-compose up --build
```

### Access container shell:
```bash
docker exec -it askmydoc-backend /bin/bash
docker exec -it askmydoc-nginx /bin/sh
```

## Security Notes

- Change default ports in production
- Use secrets management for API keys
- Enable HTTPS with SSL certificates
- Configure firewall rules
- Use Azure Key Vault for sensitive data
