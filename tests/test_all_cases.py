#!/usr/bin/env python3
"""
Test script to run all test cases from tests/excels directory
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

def test_case(name, file_paths, question):
    """Test a single case"""
    print(f"\n{'='*80}")
    print(f"TEST CASE: {name}")
    print(f"{'='*80}")
    print(f"Question: {question}")
    print(f"Files: {', '.join([Path(f).name for f in file_paths])}")
    print("\nUploading files...")
    
    try:
        upload_result = upload_files(file_paths)
        print(f"✓ Upload successful: {upload_result['tables_created']} tables created")
        print(f"  Total rows: {upload_result['row_count']}")
        
        print("\nAsking question...")
        time.sleep(1)  # Small delay to ensure processing
        
        result = ask_question(question)
        
        print(f"\n{'─'*80}")
        print("RESULT:")
        print(f"{'─'*80}")
        print(f"Model: {result['model']}")
        print(f"\nAnswer:")
        print(result['answer'])
        
        if result.get('sql_queries'):
            print(f"\nSQL Queries Used:")
            for i, query in enumerate(result['sql_queries'], 1):
                print(f"  {i}. {query}")
        
        print(f"\n{'─'*80}")
        print("✓ Test completed successfully")
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all test cases"""
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
    
    print("="*80)
    print("ASKMYDOC - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print(f"Testing {len(test_cases)} test cases against API: {API_BASE_URL}")
    print("="*80)
    
    # Check if server is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"✗ Server health check failed: {response.status_code}")
            return
        print("✓ Server is running")
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to server at {API_BASE_URL}")
        print(f"  Error: {e}")
        print("\nPlease make sure the backend server is running:")
        print("  cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload")
        return
    
    results = []
    for i, test_case_data in enumerate(test_cases, 1):
        success = test_case(
            f"{i}. {test_case_data['name']}",
            test_case_data['files'],
            test_case_data['question']
        )
        results.append((test_case_data['name'], success))
        time.sleep(2)  # Delay between tests
    
    # Summary
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n{'─'*80}")
    print(f"Total: {passed}/{total} tests passed")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()

