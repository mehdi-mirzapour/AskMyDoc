#!/usr/bin/env python3
"""
Quick solution: Upload test files to file.io and get public URLs
"""

import requests
import json

def upload_to_fileio(filepath, filename):
    """Upload file to file.io and return public URL"""
    try:
        with open(filepath, 'rb') as f:
            response = requests.post(
                'https://file.io',
                files={'file': (filename, f)},
                data={'expires': '1d'}  # File expires in 1 day
            )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return result['link']
        return None
    except Exception as e:
        print(f"Error uploading {filename}: {e}")
        return None

# Upload the two test files
files_to_upload = [
    ('tests/excels/q1_revenue_by_country/sales_2023.xlsx', 'sales_2023.xlsx'),
    ('tests/excels/q1_revenue_by_country/sales_2024.xlsx', 'sales_2024.xlsx'),
]

print("📤 Uploading files to file.io...")
print("=" * 80)

urls = []
for filepath, filename in files_to_upload:
    print(f"Uploading {filename}...")
    url = upload_to_fileio(filepath, filename)
    if url:
        print(f"✅ {filename}: {url}")
        urls.append(url)
    else:
        print(f"❌ Failed to upload {filename}")

print("=" * 80)

if len(urls) == 2:
    # Generate curl command
    curl_command = f"""curl -X POST 'http://askmydoc-app.westeurope.azurecontainer.io/api/agent_excel/' \\
  -H 'Content-Type: application/json' \\
  -d '{{
    "excel_urls": [
      "{urls[0]}",
      "{urls[1]}"
    ],
    "query": "What is the total revenue?"
  }}'"""
    
    print("\n📋 CURL COMMAND:")
    print("=" * 80)
    print(curl_command)
    print("=" * 80)
else:
    print("\n❌ Not all files uploaded successfully")
