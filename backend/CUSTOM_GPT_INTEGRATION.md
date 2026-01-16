# Custom GPT Integration Guide

## ✅ Backend Updated for Custom GPT Support

Your API now supports **both** methods:
1. **Custom GPT**: Uses `openaiFileIdRefs` (file objects with `download_link`)
2. **Direct API**: Uses `excel_urls` (direct URLs)

---

## OpenAPI Schema for Custom GPT

Use this schema in your Custom GPT Actions:

**File**: [`backend/openapi_custom_gpt.yaml`](file:///Users/mehdi/work/AskMyDoc/backend/openapi_custom_gpt.yaml)

Key points:
- ✅ Parameter name: `openaiFileIdRefs` (required by OpenAI)
- ✅ Type: `array` of `string` (OpenAI populates with objects at runtime)
- ✅ Supports up to 10 files
- ✅ URLs valid for 5 minutes

---

## Custom GPT Instructions

Add these instructions to your Custom GPT:

```
When users upload Excel files and ask questions:

1. Use the queryExcelAgent action
2. Pass the uploaded files via openaiFileIdRefs
3. Include the user's question in the query parameter
4. Present the answer in a clear, formatted way

Important:
- Only Excel files (.xlsx, .xls) are supported
- Maximum 10 files per request
- File download URLs are valid for 5 minutes
```

---

## How It Works

### What ChatGPT Sends:
```json
{
  "openaiFileIdRefs": [
    {
      "name": "sales_2023.xlsx",
      "id": "file-abc123",
      "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "download_link": "https://files.oaiusercontent.com/file-abc123/download?..."
    },
    {
      "name": "sales_2024.xlsx",
      "id": "file-def456",
      "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "download_link": "https://files.oaiusercontent.com/file-def456/download?..."
    }
  ],
  "query": "What is the total revenue?"
}
```

### What Your Backend Does:
1. Extracts `download_link` from each file object
2. Downloads Excel files from those URLs
3. Processes the data
4. Returns the answer

---

## Testing

### Test with Direct API (still works):
```bash
curl -X POST 'http://askmydoc-app.westeurope.azurecontainer.io/api/agent_excel/' \
  -H 'Content-Type: application/json' \
  -d '{
    "excel_urls": [
      "https://raw.githubusercontent.com/mehdi-mirzapour/AskMyDoc/main/tests/excels/q1_revenue_by_country/sales_2023.xlsx"
    ],
    "query": "What is the total revenue?"
  }'
```

### Test with Custom GPT:
1. Upload Excel files in ChatGPT
2. Ask: "What is the total revenue?"
3. ChatGPT calls your API with `openaiFileIdRefs`
4. Your API extracts URLs and processes files

---

## Deployment

To deploy the updated backend:

```bash
git add backend/
git commit -m "Add Custom GPT support with openaiFileIdRefs"
git push origin main
```

The GitHub Actions workflow will automatically deploy to Azure.

---

## Summary

✅ **Backend Changes:**
- Updated `AgentExcelRequest` schema to accept both `excel_urls` and `openaiFileIdRefs`
- Added logic to extract `download_link` from file objects
- Maintains backward compatibility with direct API calls

✅ **OpenAPI Schema:**
- Uses `openaiFileIdRefs` parameter as required by OpenAI
- Properly documented for Custom GPT integration

✅ **Ready to Use:**
- No further backend changes needed
- Just add the OpenAPI schema to your Custom GPT
- Add the instructions to guide ChatGPT
