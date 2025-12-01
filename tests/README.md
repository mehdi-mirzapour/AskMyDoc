# Test Excel Files

This directory contains test Excel files for the AI-powered document assistant. Each subdirectory corresponds to one of the example questions the system should be able to answer.

## Directory Structure

```
tests/excels/
├── q1_revenue_by_country/      # "Compute the total revenue per country across all files"
│   ├── question.txt            # The question to answer
│   ├── sales_2023.xlsx         # 50 sales records from 2023 (6 countries)
│   └── sales_2024.xlsx         # 60 sales records from 2024 (6 countries)
│
├── q2_highest_margin/          # "Which product has the highest average margin?"
│   ├── question.txt            # The question to answer
│   ├── products_store_a.xlsx   # 6 products with margins from Store A
│   └── products_store_b.xlsx   # 6 products with margins from Store B (some overlap)
│
├── q3_q1_vs_q2/                # "Compare sales between Q1 and Q2"
│   ├── question.txt            # The question to answer
│   ├── q1_sales.xlsx           # 40 sales from Jan-Mar 2024
│   └── q2_sales.xlsx           # 50 sales from Apr-Jun 2024
│
├── q4_top_customers/           # "List the top 5 customers by total spend"
│   ├── question.txt            # The question to answer
│   ├── online_orders.xlsx      # 80 online orders from 10 customers
│   └── retail_orders.xlsx      # 70 retail orders from 10 customers
│
└── q5_missing_values/          # "Highlight any missing values or inconsistencies"
    ├── question.txt            # The question to answer
    ├── inventory_warehouse_1.xlsx  # 8 items with missing product names, quantities, prices
    └── inventory_warehouse_2.xlsx  # 7 items with missing values, negative quantity, duplicate SKU
```

## Data Characteristics

### Q1: Revenue by Country
- **Files**: 2 (sales_2023.xlsx, sales_2024.xlsx)
- **Total Records**: 110
- **Countries**: USA, France, Germany, UK, Spain, Italy, Canada, Japan
- **Revenue Range**: $500 - $6,000 per order
- **Expected Answer**: Total revenue grouped by country across both years

### Q2: Highest Margin
- **Files**: 2 (products_store_a.xlsx, products_store_b.xlsx)
- **Total Products**: 12 (some products appear in both stores)
- **Margin Range**: 0.19 - 0.48 (19% - 48%)
- **Expected Answer**: "Gadget X" with average margin of 0.465 (46.5%)

### Q3: Q1 vs Q2 Comparison
- **Files**: 2 (q1_sales.xlsx, q2_sales.xlsx)
- **Q1 Records**: 40 (Jan-Mar 2024)
- **Q2 Records**: 50 (Apr-Jun 2024)
- **Products**: Product A, B, C, D, E
- **Expected Answer**: Comparison showing Q2 has more sales and likely higher total revenue

### Q4: Top Customers
- **Files**: 2 (online_orders.xlsx, retail_orders.xlsx)
- **Total Orders**: 150
- **Customers**: 10 unique customers
- **Order Range**: $30 - $1,500
- **Expected Answer**: Top 5 customers ranked by total spend across both channels

### Q5: Missing Values & Inconsistencies
- **Files**: 2 (inventory_warehouse_1.xlsx, inventory_warehouse_2.xlsx)
- **Issues in Warehouse 1**:
  - 2 missing product names
  - 2 missing quantities
  - 1 missing unit price
- **Issues in Warehouse 2**:
  - 1 missing product name
  - 1 missing quantity
  - 1 missing unit price
  - 1 negative quantity (-10)
  - 1 duplicate SKU (SKU009)
- **Expected Answer**: Detailed report of all missing values and data quality issues

## Generating the Files

To regenerate the test files:

```bash
python3 tests/generate_test_excels.py
```

To verify the generated files:

```bash
python3 tests/verify_excels.py
```

## Usage in Testing

These files should be used to test the AI document assistant's ability to:

1. ✅ Load multiple Excel files simultaneously
2. ✅ Convert DataFrames to SQL tables
3. ✅ Generate appropriate SQL queries from natural language
4. ✅ Perform aggregations across multiple files
5. ✅ Handle joins between related tables
6. ✅ Detect and report data quality issues
7. ✅ Compare time-based data (quarters, years)
8. ✅ Rank and filter results (top N queries)
