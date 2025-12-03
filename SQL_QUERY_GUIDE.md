# Direct SQL Query Access

## Overview
You can now query the in-memory SQLite database directly using the `/query/sql` endpoint while the backend server is running.

## Endpoint
**POST** `/query/sql`

## Request Format
```json
{
  "query": "SELECT * FROM table_name LIMIT 10"
}
```

## Response Format
```json
{
  "query": "SELECT * FROM table_name LIMIT 10",
  "columns": ["column1", "column2", "column3"],
  "rows": [
    ["value1", "value2", "value3"],
    ["value4", "value5", "value6"]
  ],
  "row_count": 2,
  "status": "success"
}
```

## Usage Examples

### 1. List all tables
```bash
curl -X POST http://localhost:8000/query/sql \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT name FROM sqlite_master WHERE type='\''table'\''"}'
```

### 2. View table schema
```bash
curl -X POST http://localhost:8000/query/sql \
  -H "Content-Type: application/json" \
  -d '{"query": "PRAGMA table_info(your_table_name)"}'
```

### 3. Query data
```bash
curl -X POST http://localhost:8000/query/sql \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM your_table_name LIMIT 10"}'
```

### 4. Aggregate queries
```bash
curl -X POST http://localhost:8000/query/sql \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT COUNT(*) as total FROM your_table_name"}'
```

### 5. Filtered queries
```bash
curl -X POST http://localhost:8000/query/sql \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM products WHERE LOWER(product_name) LIKE '\''%widget%'\''"}'
```

## Important Notes

⚠️ **Database Persistence**: The database is in-memory only (`:memory:`). It will be cleared when you restart the backend server.

⚠️ **Read-Only Recommended**: While you can execute any SQL (including INSERT/UPDATE/DELETE), it's recommended to use this endpoint for SELECT queries only to avoid unintended data modifications.

⚠️ **Error Handling**: Invalid SQL will return a 400 error with details about what went wrong.

## Using with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/query/sql",
    json={"query": "SELECT * FROM your_table LIMIT 5"}
)

data = response.json()
print(f"Columns: {data['columns']}")
print(f"Rows: {data['rows']}")
print(f"Total rows: {data['row_count']}")
```

## Using with JavaScript

```javascript
const response = await fetch('http://localhost:8000/query/sql', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'SELECT * FROM your_table LIMIT 5'
  })
});

const data = await response.json();
console.log('Columns:', data.columns);
console.log('Rows:', data.rows);
console.log('Total rows:', data.row_count);
```
