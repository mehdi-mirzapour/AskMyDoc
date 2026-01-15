"""
Test for agent_excel endpoint
Tests the new endpoint that accepts URLs and queries in a single call
"""

import pytest
import requests
import json
from pathlib import Path
import http.server
import socketserver
import threading
import time

# API Configuration
API_BASE_URL = "http://localhost:5888"
AGENT_EXCEL_ENDPOINT = f"{API_BASE_URL}/agent_excel/"

# Test data paths
TESTS_DIR = Path(__file__).parent.parent.parent / "tests" / "excels"

# Local file server configuration
FILE_SERVER_PORT = 8765
FILE_SERVER_URL = f"http://localhost:{FILE_SERVER_PORT}"


class FileServerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve files from tests directory"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(TESTS_DIR), **kwargs)
    
    def log_message(self, format, *args):
        """Suppress server logs"""
        pass


def start_file_server():
    """Start a local HTTP server to serve test Excel files"""
    handler = FileServerHandler
    with socketserver.TCPServer(("", FILE_SERVER_PORT), handler) as httpd:
        httpd.serve_forever()


@pytest.fixture(scope="module", autouse=True)
def file_server():
    """Start file server before tests and stop after"""
    server_thread = threading.Thread(target=start_file_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Give server time to start
    yield
    # Server will stop when tests complete (daemon thread)


class TestAgentExcel:
    """Test the agent_excel endpoint with all baseline test cases"""
    
    def get_file_urls(self, test_case_dir: str):
        """Helper to get URLs for Excel files in a test case directory"""
        test_path = TESTS_DIR / test_case_dir
        urls = []
        
        for excel_file in test_path.glob("*.xlsx"):
            # Construct URL for the file
            relative_path = f"{test_case_dir}/{excel_file.name}"
            url = f"{FILE_SERVER_URL}/{relative_path}"
            urls.append(url)
        
        return urls
    
    def test_q1_revenue_by_country(self):
        """Q1: Compute the total revenue per country across all files"""
        excel_urls = self.get_file_urls("q1_revenue_by_country")
        question = "Compute the total revenue per country across all files."
        
        print(f"\n=== Q1: Revenue by Country (Agent Excel) ===")
        print(f"Excel URLs: {excel_urls}")
        
        response = requests.post(
            AGENT_EXCEL_ENDPOINT,
            json={
                "query": question,
                "excel_urls": excel_urls
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        print(f"\nResponse:")
        print(f"Answer: {data.get('answer')}")
        print(f"Files Processed: {data.get('files_processed')}")
        print(f"Tables Created: {data.get('tables_created')}")
        print(f"SQL Queries: {data.get('sql_queries')}")
        
        assert "answer" in data
        assert data["files_processed"] == len(excel_urls)
        print(f"\n✓ Q1 Agent Excel Test Passed")
    
    def test_q2_highest_margin(self):
        """Q2: Which product has the highest average margin?"""
        excel_urls = self.get_file_urls("q2_highest_margin")
        question = "Which product has the highest average margin?"
        
        print(f"\n=== Q2: Highest Margin (Agent Excel) ===")
        
        response = requests.post(
            AGENT_EXCEL_ENDPOINT,
            json={
                "query": question,
                "excel_urls": excel_urls
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        print(f"\nAnswer: {data.get('answer')}")
        
        assert "answer" in data
        assert data["files_processed"] == len(excel_urls)
        print(f"\n✓ Q2 Agent Excel Test Passed")
    
    def test_q3_q1_vs_q2(self):
        """Q3: Compare sales between Q1 and Q2"""
        excel_urls = self.get_file_urls("q3_q1_vs_q2")
        question = "Compare sales between Q1 and Q2."
        
        print(f"\n=== Q3: Q1 vs Q2 (Agent Excel) ===")
        
        response = requests.post(
            AGENT_EXCEL_ENDPOINT,
            json={
                "query": question,
                "excel_urls": excel_urls
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        print(f"\nAnswer: {data.get('answer')}")
        
        assert "answer" in data
        assert data["files_processed"] == len(excel_urls)
        print(f"\n✓ Q3 Agent Excel Test Passed")
    
    def test_q4_top_customers(self):
        """Q4: List the top 5 customers by total spend"""
        excel_urls = self.get_file_urls("q4_top_customers")
        question = "List the top 5 customers by total spend."
        
        print(f"\n=== Q4: Top Customers (Agent Excel) ===")
        
        response = requests.post(
            AGENT_EXCEL_ENDPOINT,
            json={
                "query": question,
                "excel_urls": excel_urls
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        print(f"\nAnswer: {data.get('answer')}")
        
        assert "answer" in data
        assert data["files_processed"] == len(excel_urls)
        print(f"\n✓ Q4 Agent Excel Test Passed")
    
    def test_q5_missing_values(self):
        """Q5: Highlight any missing values or inconsistencies"""
        excel_urls = self.get_file_urls("q5_missing_values")
        question = "Highlight any missing values or inconsistencies."
        
        print(f"\n=== Q5: Missing Values (Agent Excel) ===")
        
        response = requests.post(
            AGENT_EXCEL_ENDPOINT,
            json={
                "query": question,
                "excel_urls": excel_urls
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        print(f"\nAnswer: {data.get('answer')}")
        
        assert "answer" in data
        assert data["files_processed"] == len(excel_urls)
        print(f"\n✓ Q5 Agent Excel Test Passed")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
