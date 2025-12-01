import pandas as pd
import os

print("=" * 80)
print("TEST EXCEL FILES VERIFICATION")
print("=" * 80)

# Q1: Revenue by country
print("\n📊 Q1: Compute total revenue per country across all files")
print("-" * 80)
sales_2023 = pd.read_excel('tests/excels/q1_revenue_by_country/sales_2023.xlsx')
sales_2024 = pd.read_excel('tests/excels/q1_revenue_by_country/sales_2024.xlsx')
print(f"sales_2023.xlsx: {len(sales_2023)} rows")
print(sales_2023.head(3))
print(f"\nsales_2024.xlsx: {len(sales_2024)} rows")
print(sales_2024.head(3))

# Q2: Highest margin
print("\n\n📊 Q2: Which product has the highest average margin?")
print("-" * 80)
products_a = pd.read_excel('tests/excels/q2_highest_margin/products_store_a.xlsx')
products_b = pd.read_excel('tests/excels/q2_highest_margin/products_store_b.xlsx')
print(f"products_store_a.xlsx: {len(products_a)} rows")
print(products_a)
print(f"\nproducts_store_b.xlsx: {len(products_b)} rows")
print(products_b)

# Q3: Q1 vs Q2
print("\n\n📊 Q3: Compare sales between Q1 and Q2")
print("-" * 80)
q1 = pd.read_excel('tests/excels/q3_q1_vs_q2/q1_sales.xlsx')
q2 = pd.read_excel('tests/excels/q3_q1_vs_q2/q2_sales.xlsx')
print(f"q1_sales.xlsx: {len(q1)} rows, Date range: {q1['sale_date'].min()} to {q1['sale_date'].max()}")
print(q1.head(3))
print(f"\nq2_sales.xlsx: {len(q2)} rows, Date range: {q2['sale_date'].min()} to {q2['sale_date'].max()}")
print(q2.head(3))

# Q4: Top customers
print("\n\n📊 Q4: List top 5 customers by total spend")
print("-" * 80)
online = pd.read_excel('tests/excels/q4_top_customers/online_orders.xlsx')
retail = pd.read_excel('tests/excels/q4_top_customers/retail_orders.xlsx')
print(f"online_orders.xlsx: {len(online)} rows")
print(online.head(3))
print(f"\nretail_orders.xlsx: {len(retail)} rows")
print(retail.head(3))

# Q5: Missing values
print("\n\n📊 Q5: Highlight missing values or inconsistencies")
print("-" * 80)
inv1 = pd.read_excel('tests/excels/q5_missing_values/inventory_warehouse_1.xlsx')
inv2 = pd.read_excel('tests/excels/q5_missing_values/inventory_warehouse_2.xlsx')
print(f"inventory_warehouse_1.xlsx: {len(inv1)} rows")
print(inv1)
print(f"\nMissing values in warehouse 1:")
print(inv1.isnull().sum())
print(f"\ninventory_warehouse_2.xlsx: {len(inv2)} rows")
print(inv2)
print(f"\nMissing values in warehouse 2:")
print(inv2.isnull().sum())
print(f"\nNegative quantities in warehouse 2: {len(inv2[inv2['quantity'] < 0])}")
print(f"Duplicate SKUs in warehouse 2: {inv2['sku'].duplicated().sum()}")

print("\n" + "=" * 80)
print("✅ All test files verified successfully!")
print("=" * 80)
