# Azure Storage CI/CD Setup

## ✅ What Was Updated

Updated `.github/workflows/deploy.yml` to include Azure Storage credentials in the deployment.

### Changes Made:

1. **Added to workflow env section** (lines 46-48):
```yaml
AZURE_STORAGE_ACCOUNT: ${{ secrets.AZURE_STORAGE_ACCOUNT }}
AZURE_STORAGE_KEY: ${{ secrets.AZURE_STORAGE_KEY }}
AZURE_STORAGE_CONTAINER: ${{ secrets.AZURE_STORAGE_CONTAINER }}
```

2. **Added to backend container env vars** (lines 69-74):
```yaml
- name: AZURE_STORAGE_ACCOUNT
  value: ${AZURE_STORAGE_ACCOUNT}
- name: AZURE_STORAGE_KEY
  secureValue: ${AZURE_STORAGE_KEY}
- name: AZURE_STORAGE_CONTAINER
  value: ${AZURE_STORAGE_CONTAINER:-excel-files}
```

---

## 📋 GitHub Secrets to Add

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these 3 secrets:

| Secret Name | Value | Notes |
|-------------|-------|-------|
| `AZURE_STORAGE_ACCOUNT` | `askdocstorage` | Your storage account name |
| `AZURE_STORAGE_KEY` | `your_key_from_azure_portal` | Get from Azure Portal → Storage Account → Access Keys |
| `AZURE_STORAGE_CONTAINER` | `excel-files` | Container name (optional, defaults to excel-files) |

---

## 🚀 Deploy

Once secrets are added:

```bash
git add .
git commit -m "Add Azure Storage upload API and CI/CD configuration"
git push origin main
```

The GitHub Actions workflow will automatically:
1. Build Docker images
2. Push to Azure Container Registry
3. Deploy to Azure Container Instances
4. **Include Azure Storage credentials** in backend container

---

## ✅ Verify After Deployment

```bash
# Check storage health
curl https://askmydoc-app.westeurope.azurecontainer.io/api/storage/health

# Expected:
# {"configured": true, "container": "excel-files"}

# Upload a file
curl -X POST 'https://askmydoc-app.westeurope.azurecontainer.io/api/storage/upload' \
  -F 'file=@your_file.xlsx'
```

---

## 📝 Summary

✅ Workflow updated with Azure Storage env vars
✅ Backend container configured with credentials
✅ Ready to deploy once GitHub Secrets are added

**Next**: Add the 3 GitHub Secrets, then push to deploy!
