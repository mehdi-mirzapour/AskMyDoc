"""
Test script for the new /agent_excel/local endpoint

This demonstrates how to call the endpoint with local file paths.
"""

import requests
import json

# API endpoint
url = "http://localhost:5882/agent_excel/local"

# Example request payload
payload = {
    "query": "What is the total revenue?",
    "file_paths": [
        "/path/to/your/file1.xlsx",
        "/path/to/your/file2.xlsx"
    ]
}

# Make the request
response = requests.post(url, json=payload)

# Print the response
if response.status_code == 200:
    result = response.json()
    print("✓ Success!")
    print(f"\nQuery: {result['query']}")
    print(f"Answer: {result['answer']}")
    print(f"\nFiles processed: {result['files_processed']}")
    print(f"Tables created: {result['tables_created']}")
    print(f"Model used: {result['model']}")
    if result.get('sql_queries'):
        print(f"\nSQL Queries executed:")
        for sql in result['sql_queries']:
            print(f"  - {sql}")
else:
    print(f"✗ Error {response.status_code}")
    print(response.json())
