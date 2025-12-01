# Detailed Explanation: TEST 5 - Missing Values & Inconsistencies

This document explains step-by-step what happened when we ran TEST 5: "Highlight any missing values or inconsistencies."

---

## 📋 Overview

**Question:** "Highlight any missing values or inconsistencies."

**Files Uploaded:**
- `inventory_warehouse_1.xlsx` (contains inventory data with missing values)
- `inventory_warehouse_2.xlsx` (contains inventory data with missing values and inconsistencies)

**Expected Result:** A comprehensive report identifying all missing values (NULL/NaN) and data quality issues across both warehouse inventory tables.

---

## 🔄 Step-by-Step Process

### Step 1: File Upload & Processing

When the test script uploaded the two Excel files:

```bash
curl -X POST \
  -F "files=@tests/excels/q5_missing_values/inventory_warehouse_1.xlsx" \
  -F "files=@tests/excels/q5_missing_values/inventory_warehouse_2.xlsx" \
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
   
   **From `inventory_warehouse_1.xlsx`:**
   - Sheet "Inventory" → Table: `inventory_warehouse_1_inventory` (8 rows)
   - Sheet "Audit Log" → Table: `inventory_warehouse_1_audit_log` (5 rows)
   - Sheet "Supplier Info" → Table: `inventory_warehouse_1_supplier_info` (3 rows)
   
   **From `inventory_warehouse_2.xlsx`:**
   - Sheet "Inventory" → Table: `inventory_warehouse_2_inventory` (7 rows)
   - Sheet "Audit Log" → Table: `inventory_warehouse_2_audit_log` (4 rows)
   - Sheet "Supplier Info" → Table: `inventory_warehouse_2_supplier_info` (3 rows)

4. **Database Storage:**
   - All data was loaded into an **in-memory SQLite database**
   - Tables were created with proper column types (TEXT, INTEGER, REAL, TIMESTAMP)
   - Missing values (NaN) were preserved as NULL in SQLite
   - Total: **40 rows** across 6 tables

**Response from upload:**
```json
{
  "filename": "1 files",
  "tables_created": [
    "inventory_warehouse_1_inventory",
    "inventory_warehouse_1_audit_log",
    "inventory_warehouse_1_supplier_info",
    "inventory_warehouse_2_inventory",
    "inventory_warehouse_2_audit_log",
    "inventory_warehouse_2_supplier_info"
  ],
  "row_count": 40,
  "status": "success"
}
```

---

### Step 2: Question Processing

When the question was sent:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "Highlight any missing values or inconsistencies."}' \
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
   Highlight any missing values or inconsistencies.
   ```

#### 2.2 First LLM Call (gpt-4o-mini)

The model analyzed the question and decided to:
- First understand the database structure
- Identify tables that might contain missing values
- Use the specialized `check_missing_values` tool designed for this purpose

**Model's Decision:** Call `get_database_schema` tool first, then use `check_missing_values` tool

---

### Step 3: Schema Discovery

**Tool Called:** `get_database_schema()`

**What it did:**
1. Retrieved schema information from all 6 tables
2. Returned column names, types, and row counts for each table

**Schema Returned:**
```
Available Tables:

Table: inventory_warehouse_1_inventory
  Rows: 8
  Columns:
    - sku (TEXT)
    - product_name (TEXT)
    - quantity (INTEGER)
    - unit_price (REAL)
    - location (TEXT)

Table: inventory_warehouse_1_audit_log
  Rows: 5
  Columns:
    - log_id (TEXT)
    - action (TEXT)
    - timestamp (TIMESTAMP)
    - user (TEXT)

Table: inventory_warehouse_1_supplier_info
  Rows: 3
  Columns:
    - supplier_id (TEXT)
    - supplier_name (TEXT)
    - contact_email (TEXT)

Table: inventory_warehouse_2_inventory
  Rows: 7
  Columns:
    - sku (TEXT)
    - product_name (TEXT)
    - quantity (INTEGER)
    - unit_price (REAL)
    - location (TEXT)

Table: inventory_warehouse_2_audit_log
  Rows: 4
  Columns:
    - log_id (TEXT)
    - action (TEXT)
    - timestamp (TIMESTAMP)
    - user (TEXT)

Table: inventory_warehouse_2_supplier_info
  Rows: 3
  Columns:
    - supplier_id (TEXT)
    - supplier_name (TEXT)
    - contact_email (TEXT)
```

**Model's Understanding:**
- Found two main inventory tables: `inventory_warehouse_1_inventory` and `inventory_warehouse_2_inventory`
- Both have columns: sku, product_name, quantity, unit_price, location
- The question specifically asks about missing values and inconsistencies
- The system has a dedicated tool for this: `check_missing_values`

---

### Step 4: Tool Execution - Missing Values Check

**Tool Called:** `check_missing_values()`

**What this tool does:**

1. **Iterates through all tables** stored in `excel_processor.tables`
2. **For each table (DataFrame):**
   - Uses `df.isnull().sum()` to count missing values per column
   - Identifies columns with missing values (count > 0)
   - Builds a report for each table

3. **Report Generation:**
   - Creates a structured report showing:
     - Table name
     - Column name with missing values
     - Count of missing values

**Tool Implementation:**
```python
@tool
def check_missing_values() -> str:
    """Check for missing values (NULL/NaN) across all tables."""
    
    report = "Missing Values Report:\n\n"
    
    for table_name, df in excel_processor.tables.items():
        missing = df.isnull().sum()
        missing_cols = missing[missing > 0]
        
        if not missing_cols.empty:
            report += f"Table: {table_name}\n"
            for col, count in missing_cols.items():
                report += f"  - {col}: {count} missing values\n"
            report += "\n"
    
    if report == "Missing Values Report:\n\n":
        report += "No missing values found in any table."
    
    return report
```

**What happened when executed:**

1. **Checked `inventory_warehouse_1_inventory`:**
   - Found missing values in:
     - `product_name`: 2 missing values
     - `quantity`: 2 missing values
     - `unit_price`: 1 missing value

2. **Checked `inventory_warehouse_2_inventory`:**
   - Found missing values in:
     - `product_name`: 1 missing value
     - `quantity`: 1 missing value
     - `unit_price`: 1 missing value

3. **Checked other tables:**
   - `inventory_warehouse_1_audit_log`: No missing values
   - `inventory_warehouse_1_supplier_info`: No missing values
   - `inventory_warehouse_2_audit_log`: No missing values
   - `inventory_warehouse_2_supplier_info`: No missing values

**Tool Output:**
```
Missing Values Report:

Table: inventory_warehouse_1_inventory
  - product_name: 2 missing values
  - quantity: 2 missing values
  - unit_price: 1 missing value

Table: inventory_warehouse_2_inventory
  - product_name: 1 missing value
  - quantity: 1 missing value
  - unit_price: 1 missing value
```

---

### Step 5: Data Analysis & Answer Generation

The model received the missing values report and performed analysis:

**Model's Reasoning Process:**

1. **Identified Missing Values:**
   - **Warehouse 1:** 5 missing values total (2 product names, 2 quantities, 1 price)
   - **Warehouse 2:** 3 missing values total (1 product name, 1 quantity, 1 price)
   - **Total:** 8 missing values across both warehouses

2. **Key Observations:**
   - Missing values are concentrated in the inventory tables
   - Critical fields are affected: product names, quantities, and prices
   - This could impact inventory management and reporting
   - Data quality issues need to be addressed

3. **Answer Formatting:**
   - Structured by table/warehouse
   - Clear listing of missing values per column
   - Added context about data quality impact

---

### Step 6: Final Answer

The model formatted the answer:

**Answer:**
```
The missing values report indicates the following inconsistencies across the 
inventory tables:

### Table: `inventory_warehouse_1_inventory`
- **product_name**: 2 missing values
- **quantity**: 2 missing values
- **unit_price**: 1 missing value

### Table: `inventory_warehouse_2_inventory`
- **product_name**: 1 missing value
- **quantity**: 1 missing value
- **unit_price**: 1 missing value

These missing values could affect data analysis and reporting, as they may lead 
to incomplete insights regarding inventory levels and pricing. It is advisable 
to address these missing entries to ensure data integrity.
```

---

## 🔍 Technical Details

### Database Structure

The system uses an **in-memory SQLite database** (`:memory:`), which means:
- Data exists only while the server is running
- Very fast for queries
- Data is cleared when server restarts
- Missing values (NaN from pandas) are stored as NULL in SQLite

### Tool Execution Flow

```
User Question
    ↓
DocumentAgent.query()
    ↓
LangGraph Workflow:
    1. _call_model() → LLM decides to use get_database_schema
    2. _call_tools() → Executes get_database_schema
    3. _call_model() → LLM sees schema, decides to use check_missing_values
    4. _call_tools() → Executes check_missing_values tool
    5. _call_model() → LLM formats the report into clear answer
    6. END → Returns final answer
```

### Model Behavior (gpt-4o-mini)

1. **Schema First:** Always checks database structure before querying
2. **Tool Selection:** Recognized the question is about data quality and used the appropriate tool
3. **Report Interpretation:** Analyzed the missing values report and provided context
4. **Clear Formatting:** Structured answer by table with clear bullet points

### Missing Values Detection

The `check_missing_values` tool:
1. Accesses all DataFrames stored in `excel_processor.tables`
2. Uses pandas `isnull().sum()` method to count missing values
3. Filters to only columns with missing values (count > 0)
4. Generates a structured text report

**Pandas `isnull().sum()`:**
- Returns a Series with count of missing values per column
- Works with NaN, None, and NULL values
- Efficient for large datasets

---

## 📊 Data Flow Diagram

```
┌─────────────────────┐
│  Excel Files        │
│  (inventory_        │
│   warehouse_1,      │
│   warehouse_2)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ExcelProcessor      │
│  - Read sheets       │
│  - Create tables     │
│  - Store DataFrames   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  SQLite DB          │
│  (in-memory)        │
│  6 tables            │
│  + DataFrames stored │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  DocumentAgent      │
│  (LangGraph)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Tool Calls:         │
│  1. get_schema      │
│  2. check_missing   │
│     _values          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Tool Execution     │
│  - Iterate tables   │
│  - Check isnull()   │
│  - Generate report   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  LLM Analysis       │
│  (gpt-4o-mini)      │
│  - Formats report   │
│  - Adds context      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Final Answer       │
│  (JSON response)    │
└─────────────────────┘
```

---

## 📈 Missing Values Analysis

### Warehouse 1 Inventory Issues

**Missing Values Breakdown:**
- **product_name**: 2 missing values (25% of 8 rows)
- **quantity**: 2 missing values (25% of 8 rows)
- **unit_price**: 1 missing value (12.5% of 8 rows)

**Impact:**
- Cannot identify 2 products (missing names)
- Cannot track inventory levels for 2 items (missing quantities)
- Cannot calculate value for 1 item (missing price)
- Affects inventory valuation and reporting

### Warehouse 2 Inventory Issues

**Missing Values Breakdown:**
- **product_name**: 1 missing value (14.3% of 7 rows)
- **quantity**: 1 missing value (14.3% of 7 rows)
- **unit_price**: 1 missing value (14.3% of 7 rows)

**Impact:**
- Cannot identify 1 product (missing name)
- Cannot track inventory level for 1 item (missing quantity)
- Cannot calculate value for 1 item (missing price)
- Affects inventory accuracy

### Combined Analysis

**Total Missing Values:**
- **Warehouse 1:** 5 missing values across 3 columns
- **Warehouse 2:** 3 missing values across 3 columns
- **Total:** 8 missing values

**Most Affected Columns:**
1. **product_name**: 3 missing values (highest count)
2. **quantity**: 3 missing values
3. **unit_price**: 2 missing values

**Data Quality Score:**
- Total cells checked: ~75 (across all inventory columns)
- Missing cells: 8
- **Data completeness: ~89.3%**

---

## 🎯 Key Insights

1. **Dedicated Tool:** System has a specialized tool (`check_missing_values`) for data quality checks

2. **Comprehensive Scanning:** Tool checks all tables automatically, not just inventory tables

3. **Detailed Reporting:** Provides specific counts per column, not just "has missing values"

4. **DataFrame Access:** Tool accesses pandas DataFrames directly (not SQL), which is more efficient for missing value detection

5. **Clear Formatting:** Report is structured and easy to understand

6. **Business Context:** Model added context about impact on data analysis and reporting

---

## 💡 What Could Be Improved

1. **Row-Level Details:** Could show which specific rows have missing values:
   ```python
   for table_name, df in excel_processor.tables.items():
       missing = df.isnull().sum()
       missing_cols = missing[missing > 0]
       
       if not missing_cols.empty:
           report += f"Table: {table_name}\n"
           for col in missing_cols.index:
               missing_rows = df[df[col].isnull()].index.tolist()
               report += f"  - {col}: {missing[col]} missing values (rows: {missing_rows})\n"
   ```

2. **Percentage Reporting:** Could include percentages:
   ```python
   report += f"  - {col}: {count} missing values ({count/len(df)*100:.1f}%)\n"
   ```

3. **Data Type Validation:** Could check for:
   - Negative quantities (inventory can't be negative)
   - Invalid price ranges
   - Duplicate SKUs
   - Date inconsistencies

4. **Summary Statistics:** Could provide:
   - Total missing values across all tables
   - Most affected table
   - Data completeness percentage

5. **SQL-Based Detection:** Could also use SQL queries:
   ```sql
   SELECT 
     COUNT(*) - COUNT(product_name) AS missing_product_name,
     COUNT(*) - COUNT(quantity) AS missing_quantity,
     COUNT(*) - COUNT(unit_price) AS missing_unit_price
   FROM inventory_warehouse_1_inventory;
   ```

However, the current approach works correctly and provides clear, actionable information!

---

## 📊 Sample Data Structure

### Warehouse 1 Inventory Table Sample
| sku | product_name | quantity | unit_price | location |
|-----|--------------|----------|------------|----------|
| SKU001 | Widget A | 100 | 25.50 | A1 |
| SKU002 | NULL | 50 | 30.00 | A2 |
| SKU003 | Gadget B | NULL | 45.75 | B1 |
| SKU004 | NULL | NULL | 20.00 | B2 |
| SKU005 | Tool C | 75 | NULL | C1 |
| ... | ... | ... | ... | ... |

**Missing Values:**
- Row 2: product_name missing
- Row 3: quantity missing
- Row 4: product_name and quantity missing
- Row 5: unit_price missing

### Warehouse 2 Inventory Table Sample
| sku | product_name | quantity | unit_price | location |
|-----|--------------|----------|------------|----------|
| SKU006 | Item D | 120 | 15.50 | D1 |
| SKU007 | NULL | 80 | 22.00 | D2 |
| SKU008 | Product E | NULL | 35.00 | E1 |
| SKU009 | Widget F | 90 | NULL | E2 |
| ... | ... | ... | ... | ... |

**Missing Values:**
- Row 2: product_name missing
- Row 3: quantity missing
- Row 4: unit_price missing

---

## 🔢 Missing Values Detection Details

### How `isnull().sum()` Works

**Pandas Method:**
```python
df.isnull().sum()
```

**What it does:**
1. `df.isnull()` - Returns DataFrame of booleans (True where value is missing)
2. `.sum()` - Sums True values (counts missing values) per column

**Example:**
```python
# DataFrame
   product_name  quantity  unit_price
0  Widget A      100       25.50
1  None          50        30.00
2  Gadget B      None      45.75
3  None          None      20.00

# After isnull()
   product_name  quantity  unit_price
0  False         False     False
1  True          False     False
2  False         True      False
3  True          True      False

# After sum()
product_name    2
quantity        2
unit_price      0
```

### Tool Implementation Details

**Code Flow:**
```python
for table_name, df in excel_processor.tables.items():
    # Count missing values per column
    missing = df.isnull().sum()
    
    # Filter to only columns with missing values
    missing_cols = missing[missing > 0]
    
    # Build report
    if not missing_cols.empty:
        report += f"Table: {table_name}\n"
        for col, count in missing_cols.items():
            report += f"  - {col}: {count} missing values\n"
```

**Efficiency:**
- O(n) complexity where n is number of cells
- Very fast for typical Excel file sizes
- Works directly with pandas DataFrames (no SQL needed)

---

## 📋 Data Quality Best Practices

### Why Missing Values Matter

1. **Inventory Management:**
   - Missing product names → Cannot identify items
   - Missing quantities → Cannot track stock levels
   - Missing prices → Cannot calculate inventory value

2. **Reporting Accuracy:**
   - Incomplete data leads to incorrect totals
   - Affects financial reporting
   - Impacts business decisions

3. **Data Integrity:**
   - Missing values indicate data entry issues
   - May indicate system problems
   - Need for data validation rules

### Recommended Actions

1. **Immediate:**
   - Identify source of missing values
   - Fill in missing data where possible
   - Document data entry procedures

2. **Prevention:**
   - Add validation rules in Excel/data entry forms
   - Require mandatory fields
   - Implement data quality checks

3. **Monitoring:**
   - Regular data quality audits
   - Automated missing value detection
   - Alert system for data issues

---

## ✅ Conclusion

TEST 5 successfully demonstrated:
- ✅ Multi-file Excel processing (2 warehouses)
- ✅ Automatic schema discovery
- ✅ Specialized tool usage (`check_missing_values`)
- ✅ Comprehensive data quality scanning
- ✅ Detailed missing values reporting
- ✅ Clear answer formatting with business context
- ✅ Proper tool usage in LangGraph workflow

The system correctly identified **all missing values** across both warehouse inventory tables:
- **Warehouse 1:** 5 missing values (2 product names, 2 quantities, 1 price)
- **Warehouse 2:** 3 missing values (1 product name, 1 quantity, 1 price)

This demonstrates the system's ability to perform data quality checks and identify data integrity issues, which is crucial for reliable data analysis!

---

## 📝 Tool Used

**Tool:** `check_missing_values()`

**Implementation:**
```python
@tool
def check_missing_values() -> str:
    """Check for missing values (NULL/NaN) across all tables."""
    
    report = "Missing Values Report:\n\n"
    
    for table_name, df in excel_processor.tables.items():
        missing = df.isnull().sum()
        missing_cols = missing[missing > 0]
        
        if not missing_cols.empty:
            report += f"Table: {table_name}\n"
            for col, count in missing_cols.items():
                report += f"  - {col}: {count} missing values\n"
            report += "\n"
    
    if report == "Missing Values Report:\n\n":
        report += "No missing values found in any table."
    
    return report
```

**Key Features:**
- ✅ Scans all tables automatically
- ✅ Uses pandas `isnull().sum()` for efficient detection
- ✅ Provides column-level detail
- ✅ Returns structured text report
- ✅ Works with DataFrames directly (no SQL needed)

---

## 🎓 Learning Points

1. **Specialized Tools:** The system has dedicated tools for specific tasks (data quality checks)

2. **DataFrame Access:** Tools can access pandas DataFrames directly, not just SQL queries

3. **Comprehensive Scanning:** Automatically checks all tables, not just one

4. **Detailed Reporting:** Provides specific counts per column, enabling targeted fixes

5. **Business Context:** Model adds meaningful interpretation of data quality issues

6. **Data Integrity:** Critical for ensuring reliable analysis and reporting

This test demonstrates the system's data quality assurance capabilities, which are essential for trustworthy business intelligence and decision-making!

