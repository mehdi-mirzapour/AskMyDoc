# Azure Storage Upload API

## Overview
Upload files to Azure Blob Storage and get public URLs for use with Custom GPT.

## Endpoints

### 1. Upload Single File
```bash
POST /api/storage/upload
```

**Example:**
```bash
curl -X POST 'http://localhost:5882/api/storage/upload' \
  -F 'file=@tests/excels/q1_revenue_by_country/sales_2023.xlsx'
```

**Response:**
```json
{
  "filename": "sales_2023.xlsx",
  "public_url": "https://askmydocstorage.blob.core.windows.net/excel-files/sales_2023.xlsx",
  "size_bytes": 12345
}
```

### 2. Upload Multiple Files
```bash
POST /api/storage/upload_multiple
```

**Example:**
```bash
curl -X POST 'http://localhost:5882/api/storage/upload_multiple' \
  -F 'files=@sales_2023.xlsx' \
  -F 'files=@sales_2024.xlsx'
```

**Response:**
```json
{
  "files": [
    {
      "filename": "sales_2023.xlsx",
      "public_url": "https://...",
      "size_bytes": 12345
    },
    {
      "filename": "sales_2024.xlsx",
      "public_url": "https://...",
      "size_bytes": 67890
    }
  ],
  "total_files": 2
}
```

### 3. Health Check
```bash
GET /api/storage/health
```

---

## Setup

### 1. Install Dependencies
```bash
pip install azure-storage-blob==12.19.0
```

### 2. Configure Environment Variables
Add to `.env`:
```bash
AZURE_STORAGE_ACCOUNT=your_storage_account
AZURE_STORAGE_KEY=your_storage_key
AZURE_STORAGE_CONTAINER=excel-files  # Optional, defaults to "excel-files"
```

### 3. Create Azure Storage Account
1. Go to Azure Portal
2. Create Storage Account
3. Get Access Keys
4. Add to `.env`

---

## Usage with Custom GPT

### Workflow:
1. **Upload files** to get public URLs
2. **Use URLs** with `agent_excel` endpoint

**Example:**
```bash
# Step 1: Upload
curl -X POST 'http://localhost:5882/api/storage/upload' \
  -F 'file=@sales_2023.xlsx'

# Response: {"public_url": "https://..."}

# Step 2: Query
curl -X POST 'http://localhost:5882/api/agent_excel/' \
  -H 'Content-Type: application/json' \
  -d '{
    "excel_urls": ["https://askmydocstorage.blob.core.windows.net/excel-files/sales_2023.xlsx"],
    "query": "What is the total revenue?"
  }'
```

---

## Files Created

- `backend/app/core/azure_storage.py` - Azure Blob Storage utility
- `backend/app/api/storage.py` - Upload API endpoints
- Updated `backend/app/main.py` - Router registration
- Updated `backend/requirements.txt` - Added azure-storage-blob

---

## Cost
- Storage: ~$0.02/GB/month
- Bandwidth: First 5GB free
- **Estimated**: < $1/month for testing

---

## Testing

```bash
# Local test
python -m uvicorn app.main:app --reload --port 5882

# Upload file
curl -X POST 'http://localhost:5882/api/storage/upload' \
  -F 'file=@tests/excels/q1_revenue_by_country/sales_2023.xlsx'

# Check health
curl 'http://localhost:5882/api/storage/health'
```
