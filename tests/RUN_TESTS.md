# How to Run Tests Manually

This guide explains how to run the test suite manually for AskMyDoc.

## Prerequisites

1. **Backend server must be running**
2. **Python virtual environment activated**
3. **All dependencies installed**

## Step-by-Step Instructions

### Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd /Users/mehdi/work/AskMyDoc/backend
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

The server should start on `http://localhost:8000`

**Keep this terminal open** - the server needs to keep running.

### Step 2: Verify Server is Running

Open a **new terminal** and test the health endpoint:

```bash
curl http://localhost:8000/health
```

You should see:
```json
{"status":"healthy","database":"connected","agent":"ready"}
```

### Step 3: Run the Test Suite

In the **new terminal**, navigate to the project root and run:

```bash
cd /Users/mehdi/work/AskMyDoc
source backend/venv/bin/activate
python tests/test_all_cases.py
```

This will run all 5 test cases automatically.

### Step 4: View Detailed Results

To see detailed results for each question:

```bash
cd /Users/mehdi/work/AskMyDoc
source backend/venv/bin/activate
python tests/show_results.py
```

## Manual Testing (One Test at a Time)

If you want to test individual cases manually, follow these steps:

### Test Case 1: Revenue by Country

```bash
# Upload files
cd /Users/mehdi/work/AskMyDoc
curl -X POST -F "files=@tests/excels/q1_revenue_by_country/sales_2023.xlsx" \
           -F "files=@tests/excels/q1_revenue_by_country/sales_2024.xlsx" \
     http://localhost:8000/upload/

# Ask question
curl -X POST -H "Content-Type: application/json" \
     -d '{"question": "Compute the total revenue per country across all files."}' \
     http://localhost:8000/query/
```

### Test Case 2: Highest Margin

```bash
# Upload files
curl -X POST -F "files=@tests/excels/q2_highest_margin/products_store_a.xlsx" \
           -F "files=@tests/excels/q2_highest_margin/products_store_b.xlsx" \
     http://localhost:8000/upload/

# Ask question
curl -X POST -H "Content-Type: application/json" \
     -d '{"question": "Which product has the highest average margin?"}' \
     http://localhost:8000/query/
```

### Test Case 3: Q1 vs Q2 Comparison

```bash
# Upload files
curl -X POST -F "files=@tests/excels/q3_q1_vs_q2/q1_sales.xlsx" \
           -F "files=@tests/excels/q3_q1_vs_q2/q2_sales.xlsx" \
     http://localhost:8000/upload/

# Ask question
curl -X POST -H "Content-Type: application/json" \
     -d '{"question": "Compare sales between Q1 and Q2."}' \
     http://localhost:8000/query/
```

### Test Case 4: Top 5 Customers

```bash
# Upload files
curl -X POST -F "files=@tests/excels/q4_top_customers/online_orders.xlsx" \
           -F "files=@tests/excels/q4_top_customers/retail_orders.xlsx" \
     http://localhost:8000/upload/

# Ask question
curl -X POST -H "Content-Type: application/json" \
     -d '{"question": "List the top 5 customers by total spend."}' \
     http://localhost:8000/query/
```

### Test Case 5: Missing Values

```bash
# Upload files
curl -X POST -F "files=@tests/excels/q5_missing_values/inventory_warehouse_1.xlsx" \
           -F "files=@tests/excels/q5_missing_values/inventory_warehouse_2.xlsx" \
     http://localhost:8000/upload/

# Ask question
curl -X POST -H "Content-Type: application/json" \
     -d '{"question": "Highlight any missing values or inconsistencies."}' \
     http://localhost:8000/query/
```

## Using the Web UI

You can also test using the frontend interface:

1. **Start the frontend** (in a new terminal):
   ```bash
   cd /Users/mehdi/work/AskMyDoc/frontend
   npm run dev
   ```

2. **Open browser** to `http://localhost:3000`

3. **Upload test files** using the drag-and-drop interface

4. **Ask questions** in the chat interface

## Test Questions Reference

All test questions are stored in `tests/excels/`:

- **Q1**: `tests/excels/q1_revenue_by_country/question.txt`
- **Q2**: `tests/excels/q2_highest_margin/question.txt`
- **Q3**: `tests/excels/q3_q1_vs_q2/question.txt`
- **Q4**: `tests/excels/q4_top_customers/question.txt`
- **Q5**: `tests/excels/q5_missing_values/question.txt`

## Troubleshooting

### Server not running
```bash
# Check if server is running
curl http://localhost:8000/health

# If not, start it:
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

### Port already in use
```bash
# Kill existing process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python -m uvicorn app.main:app --port 8001
```

### Import errors
```bash
# Make sure virtual environment is activated
source backend/venv/bin/activate

# Install missing dependencies
pip install -r backend/requirements.txt
pip install requests  # For test scripts
```

### API Key issues
Make sure `backend/.env` contains:
```
OPENAI_API_KEY=your-actual-api-key-here
```

## Quick Test Script

You can also create a simple one-liner to test:

```bash
# Test a single question
cd /Users/mehdi/work/AskMyDoc && \
source backend/venv/bin/activate && \
curl -X POST -F "files=@tests/excels/q1_revenue_by_country/sales_2023.xlsx" \
           -F "files=@tests/excels/q1_revenue_by_country/sales_2024.xlsx" \
     http://localhost:8000/upload/ && \
curl -X POST -H "Content-Type: application/json" \
     -d '{"question": "Compute the total revenue per country across all files."}' \
     http://localhost:8000/query/ | python -m json.tool
```

## Expected Results

All tests should return:
- ✅ Status code: 200
- ✅ Valid JSON response with `answer`, `sql_queries`, and `model` fields
- ✅ Meaningful answers to the questions
- ✅ Appropriate SQL queries generated

## Notes

- The backend uses an in-memory database, so data is cleared between server restarts
- Each test uploads files fresh, so you can run tests multiple times
- The model used is `gpt-4o-mini` (configured in `backend/app/core/config.py`)
- API key is read from `backend/.env` file

