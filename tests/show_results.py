#!/usr/bin/env python3
"""
Show detailed results for each test question
"""
import requests
import json
import time
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def upload_files(file_paths):
    """Upload multiple files to the API"""
    files = []
    for file_path in file_paths:
        files.append(('files', (Path(file_path).name, open(file_path, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')))
    
    response = requests.post(f"{API_BASE_URL}/upload/", files=files)
    
    # Close file handles
    for _, file_tuple in files:
        file_tuple[1].close()
    
    return response.json()

def ask_question(question):
    """Ask a question to the API"""
    response = requests.post(
        f"{API_BASE_URL}/query/",
        json={"question": question}
    )
    return response.json()

def main():
    """Run all test cases and show results"""
    base_dir = Path(__file__).parent / "excels"
    
    test_cases = [
        {
            "name": "Q1: Revenue by Country",
            "files": [
                base_dir / "q1_revenue_by_country" / "sales_2023.xlsx",
                base_dir / "q1_revenue_by_country" / "sales_2024.xlsx"
            ],
            "question": "Compute the total revenue per country across all files."
        },
        {
            "name": "Q2: Highest Margin",
            "files": [
                base_dir / "q2_highest_margin" / "products_store_a.xlsx",
                base_dir / "q2_highest_margin" / "products_store_b.xlsx"
            ],
            "question": "Which product has the highest average margin?"
        },
        {
            "name": "Q3: Q1 vs Q2 Comparison",
            "files": [
                base_dir / "q3_q1_vs_q2" / "q1_sales.xlsx",
                base_dir / "q3_q1_vs_q2" / "q2_sales.xlsx"
            ],
            "question": "Compare sales between Q1 and Q2."
        },
        {
            "name": "Q4: Top 5 Customers",
            "files": [
                base_dir / "q4_top_customers" / "online_orders.xlsx",
                base_dir / "q4_top_customers" / "retail_orders.xlsx"
            ],
            "question": "List the top 5 customers by total spend."
        },
        {
            "name": "Q5: Missing Values & Inconsistencies",
            "files": [
                base_dir / "q5_missing_values" / "inventory_warehouse_1.xlsx",
                base_dir / "q5_missing_values" / "inventory_warehouse_2.xlsx"
            ],
            "question": "Highlight any missing values or inconsistencies."
        }
    ]
    
    print("="*100)
    print("ASKMYDOC - TEST RESULTS FOR EACH QUESTION")
    print("="*100)
    
    # Check if server is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"✗ Server health check failed: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to server at {API_BASE_URL}")
        print(f"  Error: {e}")
        return
    
    for i, test_case_data in enumerate(test_cases, 1):
        print(f"\n{'#'*100}")
        print(f"# TEST {i}: {test_case_data['name']}")
        print(f"{'#'*100}")
        print(f"\n📋 QUESTION:")
        print(f"   {test_case_data['question']}")
        print(f"\n📁 FILES:")
        for f in test_case_data['files']:
            print(f"   - {f.name}")
        
        try:
            # Upload files
            upload_result = upload_files(test_case_data['files'])
            time.sleep(1)
            
            # Ask question
            result = ask_question(test_case_data['question'])
            
            print(f"\n{'─'*100}")
            print("📊 ANSWER:")
            print(f"{'─'*100}")
            print(result['answer'])
            
            if result.get('sql_queries'):
                print(f"\n{'─'*100}")
                print("🔍 SQL QUERIES USED:")
                print(f"{'─'*100}")
                for j, query in enumerate(result['sql_queries'], 1):
                    print(f"\nQuery {j}:")
                    print(f"   {query}")
            
            print(f"\n{'─'*100}")
            print(f"✅ Status: Success | Model: {result['model']}")
            print(f"{'─'*100}")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        
        time.sleep(2)  # Delay between tests
    
    print(f"\n{'='*100}")
    print("ALL TESTS COMPLETED")
    print(f"{'='*100}")

if __name__ == "__main__":
    main()

