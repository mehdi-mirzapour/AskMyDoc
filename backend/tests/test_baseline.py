"""
Integration tests for AskMyDoc API
Tests all 5 baseline use cases to verify behavior before and after refactoring
"""

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


class TestBaselineCapture:
    """Capture baseline behavior for all 5 test cases"""
    
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
        
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        
        # Close file handles
        for _, file_tuple in files:
            file_tuple[1].close()
            
        return response
    
    def query(self, question: str):
        """Helper to execute a query"""
        response = requests.post(
            QUERY_ENDPOINT,
            json={"question": question}
        )
        return response
    
    def test_q1_revenue_by_country(self):
        """Q1: Compute the total revenue per country across all files"""
        # Upload files
        upload_response = self.upload_files("q1_revenue_by_country")
        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        
        print(f"\n=== Q1: Revenue by Country ===")
        print(f"Upload Status: {upload_data.get('status')}")
        print(f"Tables Created: {upload_data.get('tables_created')}")
        print(f"Row Count: {upload_data.get('row_count')}")
        
        # Execute query
        question = "Compute the total revenue per country across all files."
        query_response = self.query(question)
        assert query_response.status_code == 200
        query_data = query_response.json()
        
        print(f"\nQuery Response:")
        print(f"Answer: {query_data.get('answer')}")
        print(f"SQL Queries: {query_data.get('sql_queries')}")
        
        # Save baseline
        baseline = {
            "test_case": "q1_revenue_by_country",
            "question": question,
            "upload": upload_data,
            "response": query_data
        }
        
        with open("/tmp/baseline_q1.json", "w") as f:
            json.dump(baseline, f, indent=2)
        
        assert "answer" in query_data
        print(f"\n✓ Q1 Baseline Captured")
    
    def test_q2_highest_margin(self):
        """Q2: Which product has the highest average margin?"""
        upload_response = self.upload_files("q2_highest_margin")
        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        
        print(f"\n=== Q2: Highest Margin ===")
        print(f"Upload Status: {upload_data.get('status')}")
        
        question = "Which product has the highest average margin?"
        query_response = self.query(question)
        assert query_response.status_code == 200
        query_data = query_response.json()
        
        print(f"\nAnswer: {query_data.get('answer')}")
        
        baseline = {
            "test_case": "q2_highest_margin",
            "question": question,
            "upload": upload_data,
            "response": query_data
        }
        
        with open("/tmp/baseline_q2.json", "w") as f:
            json.dump(baseline, f, indent=2)
        
        assert "answer" in query_data
        print(f"\n✓ Q2 Baseline Captured")
    
    def test_q3_q1_vs_q2(self):
        """Q3: Compare sales between Q1 and Q2"""
        upload_response = self.upload_files("q3_q1_vs_q2")
        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        
        print(f"\n=== Q3: Q1 vs Q2 ===")
        print(f"Upload Status: {upload_data.get('status')}")
        
        question = "Compare sales between Q1 and Q2."
        query_response = self.query(question)
        assert query_response.status_code == 200
        query_data = query_response.json()
        
        print(f"\nAnswer: {query_data.get('answer')}")
        
        baseline = {
            "test_case": "q3_q1_vs_q2",
            "question": question,
            "upload": upload_data,
            "response": query_data
        }
        
        with open("/tmp/baseline_q3.json", "w") as f:
            json.dump(baseline, f, indent=2)
        
        assert "answer" in query_data
        print(f"\n✓ Q3 Baseline Captured")
    
    def test_q4_top_customers(self):
        """Q4: List the top 5 customers by total spend"""
        upload_response = self.upload_files("q4_top_customers")
        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        
        print(f"\n=== Q4: Top Customers ===")
        print(f"Upload Status: {upload_data.get('status')}")
        
        question = "List the top 5 customers by total spend."
        query_response = self.query(question)
        assert query_response.status_code == 200
        query_data = query_response.json()
        
        print(f"\nAnswer: {query_data.get('answer')}")
        
        baseline = {
            "test_case": "q4_top_customers",
            "question": question,
            "upload": upload_data,
            "response": query_data
        }
        
        with open("/tmp/baseline_q4.json", "w") as f:
            json.dump(baseline, f, indent=2)
        
        assert "answer" in query_data
        print(f"\n✓ Q4 Baseline Captured")
    
    def test_q5_missing_values(self):
        """Q5: Highlight any missing values or inconsistencies"""
        upload_response = self.upload_files("q5_missing_values")
        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        
        print(f"\n=== Q5: Missing Values ===")
        print(f"Upload Status: {upload_data.get('status')}")
        
        question = "Highlight any missing values or inconsistencies."
        query_response = self.query(question)
        assert query_response.status_code == 200
        query_data = query_response.json()
        
        print(f"\nAnswer: {query_data.get('answer')}")
        
        baseline = {
            "test_case": "q5_missing_values",
            "question": question,
            "upload": upload_data,
            "response": query_data
        }
        
        with open("/tmp/baseline_q5.json", "w") as f:
            json.dump(baseline, f, indent=2)
        
        assert "answer" in query_data
        print(f"\n✓ Q5 Baseline Captured")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
