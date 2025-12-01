# Detailed Explanation: TEST 1 - Revenue by Country

This document explains step-by-step what happened when we ran TEST 1: "Compute the total revenue per country across all files."

---

## 📋 Overview

**Question:** "Compute the total revenue per country across all files."

**Files Uploaded:**
- `sales_2023.xlsx` (contains sales data from 2023)
- `sales_2024.xlsx` (contains sales data from 2024)

**Expected Result:** Total revenue aggregated by country across both years.

---

## 🔄 Step-by-Step Process

### Step 1: File Upload & Processing

When the test script uploaded the two Excel files:

```bash
curl -X POST \
  -F "files=@tests/excels/q1_revenue_by_country/sales_2023.xlsx" \
  -F "files=@tests/excels/q1_revenue_by_country/sales_2024.xlsx" \
  http://localhost:8000/upload/
```

**What happened internally:**

1. **File Reception:**
   - FastAPI received 2 files via multipart/form-data
   - Files were saved to `backend/uploads/` directory

2. **Excel Processing:**
   - Each Excel file was opened using `pandas.ExcelFile()`
   - The system read **all sheets** from each file
   - Each sheet became a separate SQLite table

3. **Table Creation:**
   
   **From `sales_2023.xlsx`:**
   - Sheet "Sales" → Table: `sales_2023_sales` (50 rows)
   - Sheet "Sales by Region" → Table: `sales_2023_sales_by_region` (6 rows)
   - Sheet "Product Details" → Table: `sales_2023_product_details` (10 rows)
   
   **From `sales_2024.xlsx`:**
   - Sheet "Sales" → Table: `sales_2024_sales` (60 rows)
   - Sheet "Sales by Region" → Table: `sales_2024_sales_by_region` (6 rows)
   - Sheet "Product Details" → Table: `sales_2024_product_details` (10 rows)

4. **Database Storage:**
   - All data was loaded into an **in-memory SQLite database**
   - Tables were created with proper column types (TEXT, INTEGER, REAL, TIMESTAMP)
   - Total: **142 rows** across 6 tables

**Response from upload:**
```json
{
  "filename": "1 files",
  "tables_created": [
    "sales_2023_sales",
    "sales_2023_sales_by_region", 
    "sales_2023_product_details",
    "sales_2024_sales",
    "sales_2024_sales_by_region",
    "sales_2024_product_details"
  ],
  "row_count": 142,
  "status": "success"
}
```

---

### Step 2: Question Processing

When the question was sent:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "Compute the total revenue per country across all files."}' \
  http://localhost:8000/query/
```

**What happened internally:**

#### 2.1 Agent Initialization

The `DocumentAgent` (LangGraph agent) received the question and started processing:

1. **System Message Added:**
   ```
   You are a helpful data analyst assistant. You have access to a database 
   containing Excel data.
   
   Your job is to:
   1. First, use get_database_schema to understand what tables and columns are available
   2. Use execute_sql_query to run SQL queries to answer questions
   3. Use check_missing_values when asked about data quality
   4. Provide clear, accurate answers based on the data
   ```

2. **Question Added:**
   ```
   Compute the total revenue per country across all files.
   ```

#### 2.2 First LLM Call (gpt-4o-mini)

The model analyzed the question and decided to:
- First understand the database structure
- Then query the relevant tables

**Model's Decision:** Call `get_database_schema` tool first

---

### Step 3: Schema Discovery

**Tool Called:** `get_database_schema()`

**What it did:**
1. Retrieved schema information from all 6 tables
2. Returned column names, types, and row counts for each table

**Schema Returned:**
```
Available Tables:

Table: sales_2023_sales
  Rows: 50
  Columns:
    - order_id (INTEGER)
    - country (TEXT)
    - revenue (REAL)
    - date (TIMESTAMP)

Table: sales_2023_sales_by_region
  Rows: 6
  Columns:
    - country (TEXT)
    - total_revenue (REAL)
    - order_count (INTEGER)

Table: sales_2024_sales
  Rows: 60
  Columns:
    - order_id (INTEGER)
    - country (TEXT)
    - revenue (REAL)
    - date (TIMESTAMP)

Table: sales_2024_sales_by_region
  Rows: 6
  Columns:
    - country (TEXT)
    - total_revenue (REAL)
    - order_count (INTEGER)
```

**Model's Understanding:**
- Found tables with revenue data for 2023 and 2024
- Identified that both have `country` and `revenue` columns
- Recognized aggregated tables (`sales_by_region`) exist

---

### Step 4: SQL Query Generation

The model analyzed the question and schema, then generated SQL queries:

#### Query 1: 2023 Sales Data
```sql
SELECT country, SUM(revenue) AS total_revenue 
FROM sales_2023_sales 
GROUP BY country
```

**What this does:**
- Groups all sales records by country
- Sums up revenue for each country
- Returns: France, Germany, Italy, Spain, UK, USA with their totals

**Result:**
| country | total_revenue |
|---------|--------------|
| France  | 21979.48     |
| Germany | 18461.27     |
| Italy   | 22359.60     |
| Spain   | 16537.89     |
| UK      | 10833.75     |
| USA     | 35160.87     |

#### Query 2: 2023 Sales by Region (Aggregated)
```sql
SELECT country, total_revenue 
FROM sales_2023_sales_by_region
```

**What this does:**
- Retrieves pre-aggregated revenue by country
- This is a summary table (already aggregated)

**Result:**
| country | total_revenue |
|---------|--------------|
| France  | 21979.48     |
| Germany | 18461.27     |
| Italy   | 22359.60     |
| Spain   | 16537.89     |
| UK      | 10833.75     |
| USA     | 35160.87     |

#### Query 3: 2024 Sales Data
```sql
SELECT country, SUM(revenue) AS total_revenue 
FROM sales_2024_sales 
GROUP BY country
```

**Result:**
| country | total_revenue |
|---------|--------------|
| Canada  | 37493.42     |
| France  | 26083.67     |
| Germany | 34497.44     |
| Japan   | 40311.39     |
| UK      | 21878.77     |
| USA     | 33432.39     |

#### Query 4: 2024 Sales by Region (Aggregated)
```sql
SELECT country, total_revenue 
FROM sales_2024_sales_by_region
```

**Result:**
| country | total_revenue |
|---------|--------------|
| Canada  | 37493.42     |
| France  | 26083.67     |
| Germany | 34497.44     |
| Japan   | 40311.39     |
| UK      | 21878.77     |
| USA     | 33432.39     |

---

### Step 5: Data Analysis & Answer Generation

The model received all query results and performed analysis:

**Model's Reasoning Process:**

1. **Identified Data Sources:**
   - 2023 data: 6 countries (France, Germany, Italy, Spain, UK, USA)
   - 2024 data: 6 countries (Canada, France, Germany, Japan, UK, USA)

2. **Combined Revenues:**
   - For countries appearing in both years: Added 2023 + 2024
   - For countries in only one year: Used that year's value

3. **Calculations:**

   **France:**
   - 2023: $21,979.48
   - 2024: $26,083.67
   - **Total: $48,063.15**

   **Germany:**
   - 2023: $18,461.27
   - 2024: $34,497.44
   - **Total: $52,958.71**

   **Italy:**
   - 2023: $22,359.60
   - 2024: $0 (not in 2024 data)
   - **Total: $22,359.60**

   **Spain:**
   - 2023: $16,537.89
   - 2024: $0 (not in 2024 data)
   - **Total: $16,537.89**

   **UK:**
   - 2023: $10,833.75
   - 2024: $21,878.77
   - **Total: $32,712.52**

   **USA:**
   - 2023: $35,160.87
   - 2024: $33,432.39
   - **Total: $68,593.26** (highest!)

   **Canada:**
   - 2023: $0 (not in 2023 data)
   - 2024: $37,493.42
   - **Total: $37,493.42**

   **Japan:**
   - 2023: $0 (not in 2023 data)
   - 2024: $40,311.39
   - **Total: $40,311.39**

---

### Step 6: Final Answer Formatting

The model formatted the answer with:

1. **Clear Structure:**
   - Breakdown by year
   - Combined totals
   - Summary table

2. **Final Summary Table:**
   | Country | Total Revenue |
   |---------|---------------|
   | France  | $48,063.15    |
   | Germany | $52,958.71    |
   | Italy   | $22,359.60    |
   | Spain   | $16,537.89    |
   | UK      | $32,712.52    |
   | USA     | $68,593.26    |
   | Canada  | $37,493.42    |
   | Japan   | $40,311.39    |

---

## 🔍 Technical Details

### Database Structure

The system uses an **in-memory SQLite database** (`:memory:`), which means:
- Data exists only while the server is running
- Very fast for queries
- Data is cleared when server restarts
- Perfect for this use case (temporary analysis)

### Tool Execution Flow

```
User Question
    ↓
DocumentAgent.query()
    ↓
LangGraph Workflow:
    1. _call_model() → LLM decides to use get_database_schema
    2. _call_tools() → Executes get_database_schema
    3. _call_model() → LLM sees schema, decides to query tables
    4. _call_tools() → Executes execute_sql_query (multiple times)
    5. _call_model() → LLM analyzes results, generates answer
    6. END → Returns final answer
```

### Model Behavior (gpt-4o-mini)

1. **Schema First:** Always checks database structure before querying
2. **Multiple Queries:** Queries each relevant table separately
3. **Data Combination:** Manually combines results from different tables
4. **Clear Formatting:** Structures answer with tables and explanations

### SQL Query Execution

Each SQL query:
1. Was executed via `excel_processor.execute_query()`
2. Used `pandas.read_sql_query()` to run against SQLite
3. Returned results as pandas DataFrame
4. Converted to string format for the model

---

## 📊 Data Flow Diagram

```
┌─────────────────┐
│  Excel Files    │
│  (sales_2023,   │
│   sales_2024)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ExcelProcessor  │
│  - Read sheets   │
│  - Create tables │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SQLite DB      │
│  (in-memory)    │
│  6 tables       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DocumentAgent  │
│  (LangGraph)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Tool Calls:     │
│  1. get_schema  │
│  2. execute_sql │
│     (4 queries) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Analysis   │
│  (gpt-4o-mini)  │
│  - Combines data │
│  - Calculates   │
│  - Formats      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Final Answer   │
│  (JSON response)│
└─────────────────┘
```

---

## 🎯 Key Insights

1. **Multi-file Processing:** System successfully handled 2 Excel files with multiple sheets each

2. **Schema Discovery:** Model intelligently queried schema first to understand data structure

3. **Multiple Queries:** Generated 4 separate SQL queries to gather all relevant data

4. **Data Aggregation:** Combined data from different years and tables correctly

5. **Answer Quality:** Provided clear, structured answer with breakdown and summary table

6. **Tool Usage:** Effectively used available tools (`get_database_schema`, `execute_sql_query`)

---

## 💡 What Could Be Improved

1. **Single Query:** Could use a UNION ALL to combine all sales in one query:
   ```sql
   SELECT country, SUM(revenue) AS total_revenue
   FROM (
     SELECT country, revenue FROM sales_2023_sales
     UNION ALL
     SELECT country, revenue FROM sales_2024_sales
   ) AS combined
   GROUP BY country
   ORDER BY total_revenue DESC
   ```

2. **Avoid Duplicate Queries:** The model queried both detail tables AND summary tables, which had duplicate data

3. **Better Aggregation:** Could aggregate across both files in a single step

However, the current approach works correctly and provides transparent, step-by-step reasoning!

---

## ✅ Conclusion

TEST 1 successfully demonstrated:
- ✅ Multi-file Excel processing
- ✅ Automatic schema discovery
- ✅ Intelligent SQL query generation
- ✅ Cross-table data aggregation
- ✅ Clear answer formatting
- ✅ Proper tool usage in LangGraph workflow

The system correctly computed total revenue per country across both files, showing that the AI agent can handle complex multi-file analysis tasks!

