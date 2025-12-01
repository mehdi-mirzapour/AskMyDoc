import requests
import os
import glob

API_URL = "http://localhost:8000"

def test_upload_and_query():
    print("🚀 Starting API Verification...")
    
    # 1. Upload Files
    upload_url = f"{API_URL}/upload/"
    files_to_upload = []
    
    # Collect all test files
    test_files = glob.glob("tests/excels/**/*.xlsx", recursive=True)
    print(f"Found {len(test_files)} files to upload.")
    
    files_payload = []
    opened_files = []
    
    try:
        for file_path in test_files:
            f = open(file_path, 'rb')
            opened_files.append(f)
            files_payload.append(('files', (os.path.basename(file_path), f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')))
        
        print("Uploading files...")
        response = requests.post(upload_url, files=files_payload)
        
        if response.status_code == 200:
            print("✅ Upload successful!")
            print(response.json())
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(response.text)
            return
            
    finally:
        for f in opened_files:
            f.close()
            
    # 2. Ask Questions
    questions = [
        "Compute the total revenue per country across all files",
        "Which product has the highest average margin?",
        "Compare sales between Q1 and Q2",
        "List the top 5 customers by total spend",
        "Highlight any missing values or inconsistencies"
    ]
    
    query_url = f"{API_URL}/query/"
    
    print("\n❓ Testing Questions:")
    for q in questions:
        print(f"\nAsking: {q}")
        try:
            response = requests.post(query_url, json={"question": q})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Answer: {data['answer']}")
                print(f"   Model: {data['model']}")
                if data.get('sql_queries'):
                    print(f"   SQL: {data['sql_queries'][0]}...")
            else:
                print(f"❌ Query failed: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_upload_and_query()
