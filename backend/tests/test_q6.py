
import pytest
import requests
import json
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:8000"
UPLOAD_ENDPOINT = f"{API_BASE_URL}/upload/"
QUERY_ENDPOINT = f"{API_BASE_URL}/query/"

# Test data paths
TESTS_DIR = Path(__file__).parent.parent.parent / "tests" / "excels"

class TestQ6Problematic:
    """Test Q6 Problematic Case"""
    
    def upload_files(self, test_case_dir: str):
        """Helper to upload files for a test case"""
        test_path = TESTS_DIR / test_case_dir
        files = []
        
        # Find all excel files in the test directory
        for excel_file in test_path.glob("*.xlsx"):
            files.append(
                ('files', (excel_file.name, open(excel_file, 'rb'), 
                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
            )
        
        print(f"\nUploading {len(files)} files from {test_case_dir}...")
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        
        # Close file handles
        for _, file_tuple in files:
            file_tuple[1].close()
            
        return response
    
    def query(self, question: str):
        """Helper to execute a query"""
        print(f"Asking question: {question}")
        response = requests.post(
            QUERY_ENDPOINT,
            json={"question": question}
        )
        return response
    
    def test_q6_evolution_revenue(self):
        """Q6: What was the evolution of revenue from October 8 to October 16?"""
        # Upload files
        upload_response = self.upload_files("q6_problematic_case")
        
        if upload_response.status_code != 200:
            print(f"Upload Failed: {upload_response.text}")
        
        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        
        print(f"\n=== Q6: Evolution of Revenue ===")
        print(f"Upload Status: {upload_data.get('status')}")
        print(f"Tables Created: {upload_data.get('tables_created')}")
        print(f"Row Count: {upload_data.get('row_count')}")
        
        # Execute query
        question = "What was the evolution of revenue from October 8 to October 16?"
        query_response = self.query(question)
        
        if query_response.status_code != 200:
            print(f"Query Failed: {query_response.text}")
            
        assert query_response.status_code == 200
        query_data = query_response.json()
        
        print(f"\nQuery Response:")
        print(f"Answer: {query_data.get('answer')}")
        print(f"SQL Queries: {query_data.get('sql_queries')}")
        
        # Save result
        result = {
            "test_case": "q6_problematic_case",
            "question": question,
            "upload": upload_data,
            "response": query_data
        }
        
        with open("/tmp/result_q6.json", "w") as f:
            json.dump(result, f, indent=2)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
