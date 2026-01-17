# Custom GPT Instructions for File Handling

## Based on OpenAI's File Handling Documentation

When users upload Excel files and ask questions, follow these steps:

### Step 1: Extract File URLs
When files are uploaded, you receive them as `openaiFileIdRefs`. Each file object contains a temporary download URL.

### Step 2: Call the API
Transform the file references into the format expected by the API:

```json
{
  "excel_urls": [
    "https://files.oaiusercontent.com/file-abc123...",
    "https://files.oaiusercontent.com/file-def456..."
  ],
  "query": "user's question here"
}
```

### Step 3: Important Notes
- Extract the download URL from each file in `openaiFileIdRefs`
- The download URLs are temporary and expire after a short time
- Only send Excel files (.xlsx, .xls)
- Maximum 10 files per request
- Always include both `excel_urls` and `query` parameters

### Example Transformation

**What ChatGPT receives:**
```json
{
  "openaiFileIdRefs": [
    {
      "id": "file-abc123",
      "name": "sales_2023.xlsx",
      "download_url": "https://files.oaiusercontent.com/file-abc123/download"
    }
  ]
}
```

**What to send to the API:**
```json
{
  "excel_urls": [
    "https://files.oaiusercontent.com/file-abc123/download"
  ],
  "query": "What is the total revenue?"
}
```

---

## Custom GPT Instructions

Add this to your Custom GPT:

```
When users upload Excel files:

1. Extract the download_url from each file in openaiFileIdRefs
2. Call queryExcelAgent with:
   - excel_urls: array of download URLs
   - query: the user's question
3. Present the answer clearly

Important:
- Only process Excel files (.xlsx, .xls)
- Maximum 10 files per request
- Always validate files are Excel format before calling
```
