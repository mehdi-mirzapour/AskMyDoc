import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def save_excel_multi_sheet(sheets_dict, path):
    """Saves multiple DataFrames to Excel as separate sheets.
    
    Args:
        sheets_dict: Dictionary where keys are sheet names and values are DataFrames
        path: Path to save the Excel file
    """
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        for sheet_name, df in sheets_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

# ============================================================================
# Q1: Compute the total revenue per country across all files
# ============================================================================
print("Generating Q1 files: Revenue by country...")

# File 1: Sales data for 2023
countries_2023 = ['USA', 'France', 'Germany', 'UK', 'Spain', 'Italy']
sales_2023 = pd.DataFrame({
    'order_id': range(1001, 1051),
    'country': [random.choice(countries_2023) for _ in range(50)],
    'revenue': np.random.uniform(500, 5000, 50).round(2),
    'date': [datetime(2023, random.randint(1, 12), random.randint(1, 28)) for _ in range(50)]
})

# Additional sheet: Sales by Region for 2023
sales_by_region_2023 = sales_2023.groupby('country').agg({
    'revenue': 'sum',
    'order_id': 'count'
}).reset_index()
sales_by_region_2023.columns = ['country', 'total_revenue', 'order_count']

# Additional sheet: Product Details for 2023
products_2023 = pd.DataFrame({
    'product_id': [f'P{i:03d}' for i in range(1, 11)],
    'product_name': [f'Product {chr(65+i)}' for i in range(10)],
    'category': [random.choice(['Electronics', 'Furniture', 'Clothing']) for _ in range(10)],
    'unit_price': np.random.uniform(50, 500, 10).round(2)
})

save_excel_multi_sheet({
    'Sales': sales_2023,
    'Sales by Region': sales_by_region_2023,
    'Product Details': products_2023
}, 'tests/excels/q1_revenue_by_country/sales_2023.xlsx')

# File 2: Sales data for 2024
countries_2024 = ['USA', 'France', 'Germany', 'UK', 'Canada', 'Japan']
sales_2024 = pd.DataFrame({
    'order_id': range(2001, 2061),
    'country': [random.choice(countries_2024) for _ in range(60)],
    'revenue': np.random.uniform(600, 6000, 60).round(2),
    'date': [datetime(2024, random.randint(1, 12), random.randint(1, 28)) for _ in range(60)]
})

# Additional sheet: Sales by Region for 2024
sales_by_region_2024 = sales_2024.groupby('country').agg({
    'revenue': 'sum',
    'order_id': 'count'
}).reset_index()
sales_by_region_2024.columns = ['country', 'total_revenue', 'order_count']

# Additional sheet: Product Details for 2024
products_2024 = pd.DataFrame({
    'product_id': [f'P{i:03d}' for i in range(1, 11)],
    'product_name': [f'Product {chr(65+i)}' for i in range(10)],
    'category': [random.choice(['Electronics', 'Furniture', 'Clothing']) for _ in range(10)],
    'unit_price': np.random.uniform(60, 550, 10).round(2)
})

save_excel_multi_sheet({
    'Sales': sales_2024,
    'Sales by Region': sales_by_region_2024,
    'Product Details': products_2024
}, 'tests/excels/q1_revenue_by_country/sales_2024.xlsx')

# ============================================================================
# Q2: Which product has the highest average margin?
# ============================================================================
print("Generating Q2 files: Highest average margin...")

# File 1: Product margins from Store A
products_store_a = pd.DataFrame({
    'product_id': [101, 102, 103, 104, 105, 106],
    'product_name': ['Widget A', 'Widget B', 'Gadget X', 'Gadget Y', 'Tool Z', 'Device M'],
    'margin': [0.25, 0.30, 0.45, 0.22, 0.38, 0.28],
    'store': ['Store A'] * 6
})

# Additional sheet: Inventory levels for Store A
inventory_store_a = pd.DataFrame({
    'product_id': [101, 102, 103, 104, 105, 106],
    'product_name': ['Widget A', 'Widget B', 'Gadget X', 'Gadget Y', 'Tool Z', 'Device M'],
    'stock_quantity': [150, 200, 85, 120, 95, 175],
    'reorder_level': [50, 75, 30, 40, 35, 60]
})

# Additional sheet: Pricing history for Store A
pricing_history_a = pd.DataFrame({
    'product_id': [101, 102, 103, 104, 105, 106],
    'product_name': ['Widget A', 'Widget B', 'Gadget X', 'Gadget Y', 'Tool Z', 'Device M'],
    'previous_price': [19.99, 29.99, 49.99, 39.99, 44.99, 34.99],
    'current_price': [24.99, 34.99, 54.99, 44.99, 49.99, 39.99],
    'price_change_date': [datetime(2024, 1, 15) for _ in range(6)]
})

save_excel_multi_sheet({
    'Products': products_store_a,
    'Inventory': inventory_store_a,
    'Pricing History': pricing_history_a
}, 'tests/excels/q2_highest_margin/products_store_a.xlsx')

# File 2: Product margins from Store B (some overlapping products)
products_store_b = pd.DataFrame({
    'product_id': [101, 102, 107, 108, 103, 109],
    'product_name': ['Widget A', 'Widget B', 'Gadget Z', 'Tool X', 'Gadget X', 'Device N'],
    'margin': [0.27, 0.32, 0.41, 0.19, 0.48, 0.35],
    'store': ['Store B'] * 6
})

# Additional sheet: Inventory levels for Store B
inventory_store_b = pd.DataFrame({
    'product_id': [101, 102, 107, 108, 103, 109],
    'product_name': ['Widget A', 'Widget B', 'Gadget Z', 'Tool X', 'Gadget X', 'Device N'],
    'stock_quantity': [130, 180, 75, 110, 90, 160],
    'reorder_level': [45, 70, 25, 35, 30, 55]
})

# Additional sheet: Pricing history for Store B
pricing_history_b = pd.DataFrame({
    'product_id': [101, 102, 107, 108, 103, 109],
    'product_name': ['Widget A', 'Widget B', 'Gadget Z', 'Tool X', 'Gadget X', 'Device N'],
    'previous_price': [18.99, 28.99, 47.99, 37.99, 48.99, 33.99],
    'current_price': [23.99, 33.99, 52.99, 42.99, 53.99, 38.99],
    'price_change_date': [datetime(2024, 2, 1) for _ in range(6)]
})

save_excel_multi_sheet({
    'Products': products_store_b,
    'Inventory': inventory_store_b,
    'Pricing History': pricing_history_b
}, 'tests/excels/q2_highest_margin/products_store_b.xlsx')

# ============================================================================
# Q3: Compare sales between Q1 and Q2
# ============================================================================
print("Generating Q3 files: Q1 vs Q2 comparison...")

# File 1: Sales January-March (Q1)
q1_sales = pd.DataFrame({
    'sale_id': range(3001, 3041),
    'product': [f'Product {random.choice(["A", "B", "C", "D", "E"])}' for _ in range(40)],
    'amount': np.random.uniform(100, 2000, 40).round(2),
    'sale_date': [datetime(2024, random.randint(1, 3), random.randint(1, 28)) for _ in range(40)]
})

# Additional sheet: Returns for Q1
q1_returns = pd.DataFrame({
    'return_id': range(5001, 5011),
    'sale_id': [random.choice(list(q1_sales['sale_id'])) for _ in range(10)],
    'return_amount': np.random.uniform(50, 500, 10).round(2),
    'return_date': [datetime(2024, random.randint(1, 3), random.randint(1, 28)) for _ in range(10)],
    'reason': [random.choice(['Defective', 'Wrong Item', 'Changed Mind', 'Not as Described']) for _ in range(10)]
})

# Additional sheet: Customer Feedback for Q1
q1_feedback = pd.DataFrame({
    'feedback_id': range(6001, 6021),
    'sale_id': [random.choice(list(q1_sales['sale_id'])) for _ in range(20)],
    'rating': [random.randint(1, 5) for _ in range(20)],
    'comment': [random.choice(['Great!', 'Good value', 'Fast shipping', 'Will buy again', 'Satisfied']) for _ in range(20)]
})

save_excel_multi_sheet({
    'Sales': q1_sales,
    'Returns': q1_returns,
    'Customer Feedback': q1_feedback
}, 'tests/excels/q3_q1_vs_q2/q1_sales.xlsx')

# File 2: Sales April-June (Q2)
q2_sales = pd.DataFrame({
    'sale_id': range(3041, 3091),
    'product': [f'Product {random.choice(["A", "B", "C", "D", "E"])}' for _ in range(50)],
    'amount': np.random.uniform(150, 2500, 50).round(2),
    'sale_date': [datetime(2024, random.randint(4, 6), random.randint(1, 28)) for _ in range(50)]
})

# Additional sheet: Returns for Q2
q2_returns = pd.DataFrame({
    'return_id': range(5011, 5023),
    'sale_id': [random.choice(list(q2_sales['sale_id'])) for _ in range(12)],
    'return_amount': np.random.uniform(60, 600, 12).round(2),
    'return_date': [datetime(2024, random.randint(4, 6), random.randint(1, 28)) for _ in range(12)],
    'reason': [random.choice(['Defective', 'Wrong Item', 'Changed Mind', 'Not as Described']) for _ in range(12)]
})

# Additional sheet: Customer Feedback for Q2
q2_feedback = pd.DataFrame({
    'feedback_id': range(6021, 6046),
    'sale_id': [random.choice(list(q2_sales['sale_id'])) for _ in range(25)],
    'rating': [random.randint(1, 5) for _ in range(25)],
    'comment': [random.choice(['Excellent!', 'Happy with purchase', 'Quick delivery', 'Recommended', 'Perfect']) for _ in range(25)]
})

save_excel_multi_sheet({
    'Sales': q2_sales,
    'Returns': q2_returns,
    'Customer Feedback': q2_feedback
}, 'tests/excels/q3_q1_vs_q2/q2_sales.xlsx')

# ============================================================================
# Q4: List the top 5 customers by total spend
# ============================================================================
print("Generating Q4 files: Top customers by spend...")

# File 1: Customer orders from online store
customer_names = ['Alice Johnson', 'Bob Smith', 'Carol White', 'David Brown', 'Eve Davis', 
                  'Frank Miller', 'Grace Lee', 'Henry Wilson', 'Iris Moore', 'Jack Taylor']

online_orders = pd.DataFrame({
    'order_id': range(4001, 4081),
    'customer_name': [random.choice(customer_names) for _ in range(80)],
    'order_amount': np.random.uniform(50, 1500, 80).round(2),
    'order_date': [datetime(2024, random.randint(1, 12), random.randint(1, 28)) for _ in range(80)],
    'channel': ['Online'] * 80
})

# Additional sheet: Customer Profiles
customer_profiles = pd.DataFrame({
    'customer_name': customer_names,
    'email': [f'{name.lower().replace(" ", ".")}@email.com' for name in customer_names],
    'phone': [f'+1-555-{random.randint(1000, 9999)}' for _ in range(10)],
    'loyalty_tier': [random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']) for _ in range(10)],
    'join_date': [datetime(2023, random.randint(1, 12), random.randint(1, 28)) for _ in range(10)]
})

# Additional sheet: Shipping Addresses (Online)
shipping_addresses_online = pd.DataFrame({
    'customer_name': [random.choice(customer_names) for _ in range(15)],
    'address_line1': [f'{random.randint(100, 9999)} Main St' for _ in range(15)],
    'city': [random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']) for _ in range(15)],
    'state': [random.choice(['NY', 'CA', 'IL', 'TX', 'AZ']) for _ in range(15)],
    'zip_code': [f'{random.randint(10000, 99999)}' for _ in range(15)]
})

save_excel_multi_sheet({
    'Orders': online_orders,
    'Customer Profiles': customer_profiles,
    'Shipping Addresses': shipping_addresses_online
}, 'tests/excels/q4_top_customers/online_orders.xlsx')

# File 2: Customer orders from retail store
retail_orders = pd.DataFrame({
    'order_id': range(5001, 5071),
    'customer_name': [random.choice(customer_names) for _ in range(70)],
    'order_amount': np.random.uniform(30, 1200, 70).round(2),
    'order_date': [datetime(2024, random.randint(1, 12), random.randint(1, 28)) for _ in range(70)],
    'channel': ['Retail'] * 70
})

# Additional sheet: Shipping Addresses (Retail)
shipping_addresses_retail = pd.DataFrame({
    'customer_name': [random.choice(customer_names) for _ in range(15)],
    'address_line1': [f'{random.randint(100, 9999)} Oak Ave' for _ in range(15)],
    'city': [random.choice(['Boston', 'Seattle', 'Denver', 'Miami', 'Atlanta']) for _ in range(15)],
    'state': [random.choice(['MA', 'WA', 'CO', 'FL', 'GA']) for _ in range(15)],
    'zip_code': [f'{random.randint(10000, 99999)}' for _ in range(15)]
})

save_excel_multi_sheet({
    'Orders': retail_orders,
    'Customer Profiles': customer_profiles,
    'Shipping Addresses': shipping_addresses_retail
}, 'tests/excels/q4_top_customers/retail_orders.xlsx')

# ============================================================================
# Q5: Highlight any missing values or inconsistencies
# ============================================================================
print("Generating Q5 files: Missing values and inconsistencies...")

# File 1: Inventory data with missing values
inventory_warehouse_1 = pd.DataFrame({
    'sku': ['SKU001', 'SKU002', 'SKU003', 'SKU004', 'SKU005', 'SKU006', 'SKU007', 'SKU008'],
    'product_name': ['Laptop', 'Mouse', None, 'Keyboard', 'Monitor', 'Webcam', 'Headset', None],
    'quantity': [50, 120, 75, None, 30, 45, None, 90],
    'unit_price': [899.99, 25.50, 15.99, 45.00, None, 65.00, 89.99, 12.50],
    'warehouse': ['Warehouse 1'] * 8
})

# Additional sheet: Audit Log for Warehouse 1
audit_log_1 = pd.DataFrame({
    'audit_id': range(7001, 7009),
    'sku': ['SKU001', 'SKU002', 'SKU003', 'SKU004', 'SKU005', 'SKU006', 'SKU007', 'SKU008'],
    'action': [random.choice(['Stock Added', 'Stock Removed', 'Price Updated', 'Item Checked']) for _ in range(8)],
    'timestamp': [datetime(2024, 11, random.randint(1, 30), random.randint(8, 17), random.randint(0, 59)) for _ in range(8)],
    'user': [random.choice(['Admin1', 'Manager1', 'Staff1']) for _ in range(8)]
})

# Additional sheet: Supplier Information for Warehouse 1
supplier_info_1 = pd.DataFrame({
    'supplier_id': [f'SUP{i:03d}' for i in range(1, 6)],
    'supplier_name': ['TechSupply Inc', 'Global Electronics', 'Prime Vendors', 'QuickShip Co', 'Reliable Goods'],
    'contact_email': ['contact@techsupply.com', 'sales@globalelec.com', 'info@primevendors.com', 'orders@quickship.com', 'support@reliablegoods.com'],
    'phone': ['+1-800-111-1111', '+1-800-222-2222', '+1-800-333-3333', '+1-800-444-4444', '+1-800-555-5555'],
    'rating': [4.5, 4.2, 4.8, 3.9, 4.6]
})

save_excel_multi_sheet({
    'Inventory': inventory_warehouse_1,
    'Audit Log': audit_log_1,
    'Supplier Info': supplier_info_1
}, 'tests/excels/q5_missing_values/inventory_warehouse_1.xlsx')

# File 2: Inventory data with inconsistencies (negative values, duplicates)
inventory_warehouse_2 = pd.DataFrame({
    'sku': ['SKU001', 'SKU009', 'SKU010', 'SKU011', 'SKU009', 'SKU012', 'SKU013'],  # SKU009 duplicated
    'product_name': ['Laptop', 'Tablet', 'Phone', 'Charger', 'Tablet', None, 'Cable'],
    'quantity': [45, -10, 200, 150, 85, 60, None],  # Negative quantity
    'unit_price': [899.99, 299.99, None, 19.99, 299.99, 8.50, 12.00],
    'warehouse': ['Warehouse 2'] * 7
})

# Additional sheet: Audit Log for Warehouse 2
audit_log_2 = pd.DataFrame({
    'audit_id': range(7009, 7016),
    'sku': ['SKU001', 'SKU009', 'SKU010', 'SKU011', 'SKU009', 'SKU012', 'SKU013'],
    'action': [random.choice(['Stock Added', 'Stock Removed', 'Price Updated', 'Item Checked']) for _ in range(7)],
    'timestamp': [datetime(2024, 11, random.randint(1, 30), random.randint(8, 17), random.randint(0, 59)) for _ in range(7)],
    'user': [random.choice(['Admin2', 'Manager2', 'Staff2']) for _ in range(7)]
})

# Additional sheet: Supplier Information for Warehouse 2
supplier_info_2 = pd.DataFrame({
    'supplier_id': [f'SUP{i:03d}' for i in range(6, 11)],
    'supplier_name': ['MegaSupply Ltd', 'FastTrack Wholesale', 'Quality First', 'Budget Suppliers', 'Premium Partners'],
    'contact_email': ['info@megasupply.com', 'sales@fasttrack.com', 'contact@qualityfirst.com', 'orders@budgetsup.com', 'info@premiumpart.com'],
    'phone': ['+1-800-666-6666', '+1-800-777-7777', '+1-800-888-8888', '+1-800-999-9999', '+1-800-101-0101'],
    'rating': [4.1, 4.4, 4.7, 3.5, 4.9]
})

save_excel_multi_sheet({
    'Inventory': inventory_warehouse_2,
    'Audit Log': audit_log_2,
    'Supplier Info': supplier_info_2
}, 'tests/excels/q5_missing_values/inventory_warehouse_2.xlsx')

print("\n✅ All test Excel files generated successfully!")
print("\nFile structure:")
print("tests/excels/")
print("  ├── q1_revenue_by_country/")
print("  │   ├── sales_2023.xlsx")
print("  │   └── sales_2024.xlsx")
print("  ├── q2_highest_margin/")
print("  │   ├── products_store_a.xlsx")
print("  │   └── products_store_b.xlsx")
print("  ├── q3_q1_vs_q2/")
print("  │   ├── q1_sales.xlsx")
print("  │   └── q2_sales.xlsx")
print("  ├── q4_top_customers/")
print("  │   ├── online_orders.xlsx")
print("  │   └── retail_orders.xlsx")
print("  └── q5_missing_values/")
print("      ├── inventory_warehouse_1.xlsx")
print("      └── inventory_warehouse_2.xlsx")
