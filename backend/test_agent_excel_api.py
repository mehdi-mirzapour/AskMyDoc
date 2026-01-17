#!/usr/bin/env python3
"""
Test script for agent_excel endpoint
Tests the deployed API at http://askmydoc-app.westeurope.azurecontainer.io/api/
"""

import requests
import json
from pathlib import Path

# API endpoint
API_BASE = "http://askmydoc-app.westeurope.azurecontainer.io/api"
AGENT_EXCEL_URL = f"{API_BASE}/agent_excel/"

def test_agent_excel_with_local_files():
    """
    Test agent_excel endpoint with Excel files served from local file server
    
    This test assumes you're running a local file server on port 8000
    Run: python -m http.server 8000 --directory tests/excels
    """
    
    # Example: Using files from local file server
    # Replace localhost:8000 with your actual file server URL
    excel_urls = [
        "http://localhost:8000/sales_data.xlsx",
        "http://localhost:8000/inventory.xlsx"
    ]
    
    query = "What is the total sales amount?"
    
    payload = {
        "excel_urls": excel_urls,
        "query": query
    }
    
    print(f"🚀 Testing agent_excel endpoint...")
    print(f"📊 Excel URLs: {excel_urls}")
    print(f"❓ Query: {query}")
    print(f"🌐 API URL: {AGENT_EXCEL_URL}")
    print("-" * 80)
    
    try:
        response = requests.post(AGENT_EXCEL_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        print("✅ SUCCESS!")
        print("-" * 80)
        print(f"📝 Query: {result['query']}")
        print(f"💡 Answer: {result['answer']}")
        print(f"📊 Files Processed: {result['files_processed']}")
        print(f"🗂️  Tables Created: {result['tables_created']}")
        print(f"🤖 Model: {result['model']}")
        
        if result.get('sql_queries'):
            print(f"\n🔍 SQL Queries:")
            for sql in result['sql_queries']:
                print(f"   {sql}")
        
        print("-" * 80)
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response Status: {e.response.status_code}")
            print(f"Response Body: {e.response.text}")
        return None


def test_agent_excel_with_public_urls():
    """
    Test agent_excel endpoint with publicly accessible Excel files
    """
    
    # You'll need to replace these with actual public URLs or your file server URLs
    excel_urls = [
        "YOUR_FILE_SERVER_URL/file1.xlsx",
        "YOUR_FILE_SERVER_URL/file2.xlsx"
    ]
    
    query = "What is the total revenue?"
    
    payload = {
        "excel_urls": excel_urls,
        "query": query
    }
    
    print(f"🚀 Testing agent_excel endpoint with public URLs...")
    print(f"📊 Excel URLs: {excel_urls}")
    print(f"❓ Query: {query}")
    print("-" * 80)
    
    try:
        response = requests.post(AGENT_EXCEL_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        print("✅ SUCCESS!")
        print(json.dumps(result, indent=2))
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None


def generate_curl_command(file_server_url, excel_files, query):
    """
    Generate a curl command for testing
    
    Args:
        file_server_url: Base URL of your file server (e.g., http://your-ip:8000)
        excel_files: List of Excel filenames
        query: Query string
    """
    
    excel_urls = [f"{file_server_url}/{filename}" for filename in excel_files]
    
    payload = {
        "excel_urls": excel_urls,
        "query": query
    }
    
    payload_json = json.dumps(payload, indent=2)
    
    curl_command = f"""curl -X POST '{AGENT_EXCEL_URL}' \\
  -H 'Content-Type: application/json' \\
  -d '{json.dumps(payload)}'"""
    
    print("📋 CURL COMMAND:")
    print("-" * 80)
    print(curl_command)
    print("-" * 80)
    print("\n📋 FORMATTED PAYLOAD:")
    print(payload_json)
    print("-" * 80)
    
    return curl_command


if __name__ == "__main__":
    print("=" * 80)
    print("🧪 Agent Excel API Test Script")
    print("=" * 80)
    print()
    
    # Example: Generate curl command
    # Replace with your actual file server URL and files
    print("EXAMPLE CURL COMMAND:")
    generate_curl_command(
        file_server_url="http://YOUR_IP:8000",
        excel_files=["sales_data.xlsx", "inventory.xlsx"],
        query="What is the total sales amount?"
    )
    
    print("\n" + "=" * 80)
    print("To run the test:")
    print("1. Start a file server: python -m http.server 8000 --directory tests/excels")
    print("2. Update the file server URL in this script")
    print("3. Run: python backend/test_agent_excel_api.py")
    print("=" * 80)
