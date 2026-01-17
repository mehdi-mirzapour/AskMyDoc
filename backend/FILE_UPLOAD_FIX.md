# Custom GPT File Upload Issue - Solution

## Problem
`openaiFileIdRefs` returns empty array even when files are uploaded.

## Root Causes (from research):
1. ❌ `x-openai-isConversationFileRefs` is NOT a valid OpenAPI extension
2. ❌ `openaiFileIdRefs` should NOT be in the `required` array
3. ❌ Items should be `type: string` not `type: object`
4. ⚠️ Instructions must be VERY explicit about calling the action

## ✅ Solution:

### 1. Use This Schema:
```yaml
openaiFileIdRefs:
  type: array
  description: Excel files from the conversation (auto-populated)
  items:
    type: string  # ← Must be string, not object!
```

### 2. Update Instructions (CRITICAL):
```
IMPORTANT: When users upload Excel files and ask questions, you MUST:

1. IMMEDIATELY call the queryExcelAgent action
2. DO NOT try to analyze files yourself
3. ALWAYS include uploaded files in openaiFileIdRefs parameter
4. Pass the user's question in the query parameter

Example:
User uploads files → You call queryExcelAgent → Present answer
```

### 3. Additional Fixes:
- Remove `openaiFileIdRefs` from `required` array
- Keep only `query` as required
- Use `items: type: string` (even though runtime sends objects)
- Make instructions VERY explicit about calling the action

## Try This:
1. Use schema from `backend/openapi_custom_gpt_final.yaml`
2. Update instructions to be more directive
3. Test with 1-2 files first
4. Check if files appear in openaiFileIdRefs

If still empty, it may be an intermittent OpenAI platform issue.
