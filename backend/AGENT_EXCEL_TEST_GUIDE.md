# Agent Excel API Testing Guide

## File Server Running

✅ **File server is running at**: `http://192.168.1.24:8000`

The server is serving Excel files from: `/Users/mehdi/work/AskMyDoc/tests/excels`

## Available Test Cases

### Test Case 1: Revenue by Country (Q1)
**Files**: 
- `q1_revenue_by_country/sales_2023.xlsx`
- `q1_revenue_by_country/sales_2024.xlsx`

**Query**: "What is the total revenue by country?"

**Curl Command**:
```bash
curl -X POST 'http://askmydoc-app.westeurope.azurecontainer.io/api/agent_excel/' \
  -H 'Content-Type: application/json' \
  -d '{
    "excel_urls": [
      "http://192.168.1.24:8000/q1_revenue_by_country/sales_2023.xlsx",
      "http://192.168.1.24:8000/q1_revenue_by_country/sales_2024.xlsx"
    ],
    "query": "What is the total revenue by country?"
  }'
```

---

### Test Case 2: Highest Margin Product (Q2)
**Files**:
- `q2_highest_margin/products_store_a.xlsx`
- `q2_highest_margin/products_store_b.xlsx`

**Query**: "Which product has the highest profit margin?"

**Curl Command**:
```bash
curl -X POST 'http://askmydoc-app.westeurope.azurecontainer.io/api/agent_excel/' \
  -H 'Content-Type: application/json' \
  -d '{
    "excel_urls": [
      "http://192.168.1.24:8000/q2_highest_margin/products_store_a.xlsx",
      "http://192.168.1.24:8000/q2_highest_margin/products_store_b.xlsx"
    ],
    "query": "Which product has the highest profit margin?"
  }'
```

---

### Test Case 3: Q1 vs Q2 Comparison (Q3)
**Files**:
- `q3_q1_vs_q2/q1_sales.xlsx`
- `q3_q1_vs_q2/q2_sales.xlsx`

**Query**: "Compare Q1 and Q2 sales performance"

**Curl Command**:
```bash
curl -X POST 'http://askmydoc-app.westeurope.azurecontainer.io/api/agent_excel/' \
  -H 'Content-Type: application/json' \
  -d '{
    "excel_urls": [
      "http://192.168.1.24:8000/q3_q1_vs_q2/q1_sales.xlsx",
      "http://192.168.1.24:8000/q3_q1_vs_q2/q2_sales.xlsx"
    ],
    "query": "Compare Q1 and Q2 sales performance"
  }'
```

---

### Test Case 4: Top Customers (Q4)
**Files**:
- `q4_top_customers/online_orders.xlsx`
- `q4_top_customers/retail_orders.xlsx`

**Query**: "Who are the top 5 customers by total order value?"

**Curl Command**:
```bash
curl -X POST 'http://askmydoc-app.westeurope.azurecontainer.io/api/agent_excel/' \
  -H 'Content-Type: application/json' \
  -d '{
    "excel_urls": [
      "http://192.168.1.24:8000/q4_top_customers/online_orders.xlsx",
      "http://192.168.1.24:8000/q4_top_customers/retail_orders.xlsx"
    ],
    "query": "Who are the top 5 customers by total order value?"
  }'
```

---

### Test Case 5: Missing Values (Q5)
**Files**:
- `q5_missing_values/inventory_warehouse_1.xlsx`
- `q5_missing_values/inventory_warehouse_2.xlsx`

**Query**: "What is the total inventory across all warehouses?"

**Curl Command**:
```bash
curl -X POST 'http://askmydoc-app.westeurope.azurecontainer.io/api/agent_excel/' \
  -H 'Content-Type: application/json' \
  -d '{
    "excel_urls": [
      "http://192.168.1.24:8000/q5_missing_values/inventory_warehouse_1.xlsx",
      "http://192.168.1.24:8000/q5_missing_values/inventory_warehouse_2.xlsx"
    ],
    "query": "What is the total inventory across all warehouses?"
  }'
```

---

## Quick Test (Simple)

**Simplest test with both 2023 and 2024 files**:

```bash
curl -X POST 'http://askmydoc-app.westeurope.azurecontainer.io/api/agent_excel/' \
  -H 'Content-Type: application/json' \
  -d '{
    "excel_urls": [
      "http://192.168.1.24:8000/q1_revenue_by_country/sales_2023.xlsx",
      "http://192.168.1.24:8000/q1_revenue_by_country/sales_2024.xlsx"
    ],
    "query": "What is the total revenue?"
  }'
```

---

## Using Python Test Script

Run the test script:
```bash
cd /Users/mehdi/work/AskMyDoc
python backend/test_agent_excel_api.py
```

---

## Notes

- ✅ File server is running on `http://192.168.1.24:8000`
- ✅ API endpoint: `http://askmydoc-app.westeurope.azurecontainer.io/api/agent_excel/`
- ⚠️ Make sure your firewall allows incoming connections on port 8000
- ⚠️ The Azure container needs to be able to reach your local IP (192.168.1.24)

## Stopping the File Server

To stop the file server, find the process and kill it:
```bash
lsof -ti:8000 | xargs kill -9
```

Or use the command ID to terminate it.
