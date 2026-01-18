import requests

# Define the upload URL
upload_url = "http://askmydoc-app.westeurope.azurecontainer.io/storage/upload_multiple"

# Prepare the files for upload
files = [
    ('files', open(f'{file}', 'rb'))
    for file in ['openapi_custom_gpt.yaml','test_agent_excel_api.py']
]

# Attempt to upload the files

response = requests.post(upload_url, files=files, headers={"accept": "application/json"})
upload_result = response.json()


print(upload_result)