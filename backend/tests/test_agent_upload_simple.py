"""
Simple test script for agent_upload endpoint
Demonstrates uploading files and querying in one request
"""

import requests
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:5888"
AGENT_UPLOAD_ENDPOINT = f"{API_BASE_URL}/agent_upload/"

# Test data paths
TESTS_DIR = Path(__file__).parent.parent.parent / "tests" / "excels" / "q1_revenue_by_country"

def test_agent_upload():
    """Test the agent_upload endpoint with file uploads"""
    
    # Prepare files
    files = []
    for excel_file in TESTS_DIR.glob("*.xlsx"):
        files.append(
            ('files', (excel_file.name, open(excel_file, 'rb'), 
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        )
    
    # Prepare query
    data = {
        'query': 'Compute the total revenue per country across all files.'
    }
    
    print(f"\n=== Testing Agent Upload Endpoint ===")
    print(f"Files to upload: {[f[1][0] for f in files]}")
    print(f"Query: {data['query']}")
    
    # Make request
    response = requests.post(AGENT_UPLOAD_ENDPOINT, files=files, data=data)
    
    # Close file handles
    for _, file_tuple in files:
        file_tuple[1].close()
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Success!")
        print(f"Files Processed: {result.get('files_processed')}")
        print(f"Tables Created: {result.get('tables_created')}")
        print(f"Answer: {result.get('answer')[:200]}...")
        print(f"SQL Queries: {len(result.get('sql_queries', []))} queries executed")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_agent_upload()
