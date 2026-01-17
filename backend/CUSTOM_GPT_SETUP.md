# Custom GPT Configuration for AskMyDoc Excel Agent

## Option 1: Custom GPT Instructions (Simpler - Use This)

Add these instructions to your Custom GPT:

```
When the user uploads Excel files and asks a question:

1. Extract the download URLs from the uploaded files
2. Call the queryExcelAgent action with this exact format:
   {
     "excel_urls": ["url1", "url2", ...],
     "query": "user's question"
   }

Important: 
- The parameter name must be "excel_urls" (not openaiFileIdRefs)
- Each URL should be the direct download link from the file object
- Always include both excel_urls and query in the request
```

### OpenAPI Schema to Use:
Use the file: `backend/openapi_custom_gpt.yaml`

---

## Option 2: Modify Backend to Accept openaiFileIdRefs (More Flexible)

If you want to support both formats, update your backend endpoint.

### Add to `backend/app/api/agent_excel.py`:

```python
@router.post("/", response_model=AgentExcelResponse)
async def process_excel_query(request: AgentExcelRequest):
    # Handle both excel_urls and openaiFileIdRefs
    excel_urls = request.excel_urls or []
    
    # If openaiFileIdRefs is provided, extract URLs
    if hasattr(request, 'openaiFileIdRefs') and request.openaiFileIdRefs:
        for file_ref in request.openaiFileIdRefs:
            if isinstance(file_ref, dict):
                # Extract download_url from ChatGPT file object
                url = file_ref.get('download_url') or file_ref.get('url')
                if url:
                    excel_urls.append(url)
            elif isinstance(file_ref, str):
                excel_urls.append(file_ref)
    
    if not excel_urls:
        raise HTTPException(status_code=400, detail="No Excel URLs provided")
    
    # Continue with existing logic...
```

### Update schema in `backend/app/models/schemas.py`:

```python
class AgentExcelRequest(BaseModel):
    excel_urls: Optional[List[str]] = None
    openaiFileIdRefs: Optional[List[Union[str, dict]]] = None
    query: str
    
    @validator('excel_urls', 'openaiFileIdRefs')
    def check_urls_provided(cls, v, values):
        if not values.get('excel_urls') and not values.get('openaiFileIdRefs'):
            raise ValueError('Either excel_urls or openaiFileIdRefs must be provided')
        return v
```

---

## Recommended Approach

**Use Option 1** (Custom GPT Instructions) because:
- ✅ No backend changes needed
- ✅ Works immediately
- ✅ Simpler to maintain
- ✅ ChatGPT can easily transform the data

Just add the instructions to your Custom GPT and use the OpenAPI schema from `openapi_custom_gpt.yaml`.

---

## Testing Your Custom GPT

Once configured, users can:

1. Upload Excel files in the chat
2. Ask: "What is the total revenue?"
3. ChatGPT will:
   - Extract file URLs
   - Call your API with proper format
   - Return the answer

Example user interaction:
```
User: [uploads sales_2023.xlsx and sales_2024.xlsx]
User: What is the total revenue?

ChatGPT: Let me analyze those Excel files...
[Calls your API]
ChatGPT: The total revenue across both files is $638,060.88
```
