# Technical Document - AskMyDoc

**Version:** 1.0.0  
**Date:** December 2024  
**Author:** AI Document Assistant Team

---

## 1. Architecture Overview

### System Components

The AskMyDoc system consists of three main components:

#### 1.1 Backend (FastAPI + Python)
- **Web Framework**: FastAPI for REST API
- **Data Processing**: pandas + openpyxl for Excel file handling
- **Database**: SQLite for in-memory data storage and querying
- **AI Framework**: LangChain + LangGraph for agent orchestration
- **LLM Support**: OpenAI GPT-4 and Mistral Large (switchable)
- **Monitoring**: Langfuse for AI agent tracking and observability
- **Logging**: Rich library for beautiful console logs

#### 1.2 Frontend (React)
- **Framework**: React 18 with Vite build tool
- **UI Components**: Custom-built file upload and chat interface
- **API Client**: Axios for HTTP requests
- **Styling**: Modern CSS with gradients and animations

#### 1.3 Data Flow

```
User Upload → FastAPI → Excel Processor → SQLite Database
                ↓
User Question → LangGraph Agent → Tools (SQL, Schema, etc.) → Response
```

### Architecture Diagram (Conceptual)

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  ┌──────────────┐              ┌────────────────┐           │
│  │ FileUpload   │              │ ChatInterface  │           │
│  └──────────────┘              └────────────────┘           │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/REST
┌─────────────────────┴───────────────────────────────────────┐
│                      Backend (FastAPI)                       │
│  ┌──────────────┐              ┌────────────────┐           │
│  │ Upload API   │              │ Query API      │           │
│  └──────┬───────┘              └────────┬───────┘           │
│         │                               │                   │
│  ┌──────▼───────┐              ┌────────▼───────┐           │
│  │ Excel        │              │ LangGraph      │           │
│  │ Processor    │              │ Agent          │           │
│  └──────┬───────┘              └────────┬───────┘           │
│         │                               │                   │
│  ┌──────▼───────────────────────────────▼───────┐           │
│  │               SQLite Database                 │           │
│  └───────────────────────────────────────────────┘           │
│                                                              │
│  ┌──────────────────────────────────────────────┐           │
│  │  LangChain Tools (SQL, Schema, Missing)      │           │
│  └──────────────────────────────────────────────┘           │
└──────────────────────────────────────────────────────────────┘
                      │
                      ▼
            ┌─────────────────┐
            │  OpenAI/Mistral │
            │      APIs       │
            └─────────────────┘
```

---

## 2. Current Capabilities

### 2.1 File Processing
- ✅ **Multi-file upload**: Supports uploading multiple Excel files simultaneously
- ✅ **Multiple sheets**: Reads all sheets from each Excel file
- ✅ **Data conversion**: Converts DataFrame to SQL tables in SQLite
- ✅ **Schema extraction**: Automatically extracts table schemas and metadata
- ✅ **Format support**: `.xlsx` and `.xls` files

### 2.2 Question Answering
- ✅ **Natural language queries**: Understands questions in plain English
- ✅ **SQL generation**: Automatically generates SQL queries based on questions
- ✅ **Aggregations**: Computes sums, averages, counts, groupings
- ✅ **Comparisons**: Compares data across different time periods or categories
- ✅ **Rankings**: Identifies top/bottom performers
- ✅ **Data quality checks**: Detects missing values, duplicates, inconsistencies

### 2.3 AI Agent Features
- ✅ **Tool usage**: Agent uses multiple tools (schema inspection, SQL execution, data quality checks)
- ✅ **ReAct pattern**: Agent reasons about the problem before taking action
- ✅ **Multi-step reasoning**: Can combine multiple queries to answer complex questions
- ✅ **Model flexibility**: Supports both OpenAI and Mistral (manual switch)

### 2.4 User Interface
- ✅ **Drag-and-drop upload**: Intuitive file upload interface
- ✅ **Chat interface**: Conversational Q&A experience
- ✅ **Example questions**: Pre-populated examples for quick testing
- ✅ **SQL transparency**: Shows SQL queries used to generate answers
- ✅ **Model indicator**: Displays which AI model generated the response

### 2.5 Monitoring & Logging
- ✅ **Rich console logs**: Beautiful, color-coded logs with progress indicators
- ✅ **Langfuse integration**: Tracks LLM calls, latency, and costs
- ✅ **Action tracking**: Logs every step (file upload, query execution, tool usage)

---

## 3. Limitations and What is Not Implemented

### 3.1 Data Persistence
- ❌ **No permanent storage**: Uploaded files and database are in-memory only
- ❌ **Session management**: No user sessions or authentication
- ❌ **Database resets on restart**: All data is lost when server restarts

### 3.2 Scalability
- ❌ **Single-threaded**: No async processing for large files
- ❌ **Memory constraints**: Large files (>100MB) may cause memory issues
- ❌ **No caching**: Repeated queries re-execute from scratch

### 3.3 Security
- ❌ **No authentication**: Anyone with access can upload files and query
- ❌ **No input validation**: Limited validation on file content
- ❌ **No rate limiting**: No protection against API abuse

### 3.4 AI Capabilities
- ❌ **No chart generation**: Cannot create visualizations
- ❌ **No file editing**: Cannot modify or update Excel files
- ❌ **No multi-document joins**: Limited ability to join across unrelated files
- ❌ **No streaming responses**: Responses are batch, not streamed

### 3.5 Frontend
- ❌ **No mobile optimization**: UI is desktop-focused
- ❌ **No file preview**: Cannot preview Excel content before asking questions
- ❌ **No export functionality**: Cannot export answers as PDF or Excel

---

## 4. Failure Modes

### 4.1 Common Failure Scenarios

| Scenario | Cause | Symptom | Mitigation |
|----------|-------|---------|------------|
| **Upload Failure** | Invalid file format | "Invalid file type" error | Only upload `.xlsx` or `.xls` files |
| **Query Timeout** | Complex SQL query | No response after 30s | Simplify question or break into parts |
| **SQL Error** | Invalid table/column names | "SQL execution error" | Check schema with `getSchema()` tool |
| **API Key Invalid** | Wrong/expired keys | 401 Unauthorized error | Update keys in `config.py` |
| **Memory Error** | File too large | Server crash | Limit file size to <50MB |
| **Model Hallucination** | Insufficient context | Incorrect answer | Provide more specific questions |
| **Connection Lost** | Backend not running | "Network Error" in frontend | Restart backend server |

### 4.2 Error Handling

The system includes error handling at multiple levels:
- **Frontend**: Displays user-friendly error messages
- **API**: Returns structured error responses with details
- **Agent**: Catches tool execution errors and retries
- **Logging**: All errors are logged with Rich formatting

---

## 5. Productionization Roadmap

### Phase 1: Foundation (2-3 days)
- **Database Migration**: 
  - Replace SQLite in-memory with PostgreSQL
  - Implement database migrations (Alembic)
  - Add connection pooling
  - **Estimate**: 1 day

- **File Storage**:
  - Implement cloud storage (AWS S3 or Google Cloud Storage)
  - Add file versioning
  - **Estimate**: 1 day

- **Authentication**:
  - Add JWT-based authentication
  - Implement user roles (admin, user)
  - **Estimate**: 1 day

### Phase 2: Performance & Reliability (3-4 days)
- **Caching**:
  - Add Redis for query result caching
  - Cache LLM responses for common questions
  - **Estimate**: 1 day

- **Async Processing**:
  - Implement background job queue (Celery)
  - Async file processing for large files
  - **Estimate**: 1 day

- **Error Recovery**:
  - Add retry logic with exponential backoff
  - Implement circuit breakers for external APIs
  - **Estimate**: 1 day

- **Monitoring**:
  - Add Prometheus metrics
  - Set up Grafana dashboards
  - **Estimate**: 0.5 day

### Phase 3: Features & UX (2-3 days)
- **Streaming Responses**:
  - Implement WebSocket for real-time updates
  - Stream LLM responses token-by-token
  - **Estimate**: 1 day

- **Visualization**:
  - Add chart generation (Plotly)
  - Export answers as PDF
  - **Estimate**: 1 day

- **Advanced Queries**:
  - Support for JOIN operations across files
  - Time series analysis
  - **Estimate**: 1 day

### Phase 4: Deployment (1-2 days)
- **Containerization**:
  - Create Docker images for frontend and backend
  - Docker Compose for local development
  - **Estimate**: 0.5 day

- **Cloud Deployment**:
  - Deploy to AWS ECS or GCP Cloud Run
  - Set up load balancer
  - Configure auto-scaling
  - **Estimate**: 1 day

- **CI/CD**:
  - Set up GitHub Actions for automated testing
  - Automated deployment pipeline
  - **Estimate**: 0.5 day

**Total Estimated Timeline**: 8-12 days

---

## 6. Testing Criteria

### 6.1 Functional Testing

**Test Cases**:

| ID | Test | Expected Result | Status |
|----|------|----------------|--------|
| T1 | Upload single Excel file | File loads, tables created | ✅ |
| T2 | Upload multiple Excel files | All files load correctly | ✅ |
| T3 | Upload file with multiple sheets | All sheets become separate tables | ✅ |
| T4 | Ask aggregation question (Q1) | Correct total revenue by country | ⏳ |
| T5 | Ask comparison question (Q3) | Accurate Q1 vs Q2 comparison | ⏳ |
| T6 | Ask ranking question (Q4) | Top 5 customers identified | ⏳ |
| T7 | Ask data quality question (Q5) | Missing values detected | ⏳ |
| T8 | Invalid file upload | Error message displayed | ✅ |
| T9 | Empty question submission | No action taken | ✅ |
| T10 | Switch models (OpenAI ↔ Mistral) | Both models work | ⏳ |

### 6.2 Performance Testing

- **Latency**: Response time < 10 seconds for typical questions
- **File size**: Handle files up to 50MB
- **Concurrent users**: Support 10 simultaneous users (current: 1)

### 6.3 Integration Testing

Test the full pipeline:
1. Upload `tests/excels/` files
2. Ask all 5 example questions
3. Verify answers match expected results
4. Check Langfuse logs for completeness

### 6.4 Testing Solution

**Automated Test Script** (to be implemented):

```python
# tests/test_integration.py
import pytest
from app.core.excel_processor import ExcelProcessor
from app.agents.document_agent import DocumentAgent

def test_revenue_by_country():
    processor = ExcelProcessor()
    processor.load_excel_file("tests/excels/q1_revenue_by_country/sales_2023.xlsx")
    processor.load_excel_file("tests/excels/q1_revenue_by_country/sales_2024.xlsx")
    
    agent = DocumentAgent()
    result = agent.query("Compute the total revenue per country across all files")
    
    assert "USA" in result["answer"]
    assert len(result["sql_queries"]) > 0
```

Run tests:
```bash
pytest tests/
```

---

## Appendix A: Technology Stack Details

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Backend Framework | FastAPI | 0.109.0 | REST API |
| AI Orchestration | LangGraph | 0.0.20 | Agent workflows |
| LLM Integration | LangChain | 0.1.6 | Tool abstractions |
| Database | SQLite | 3.x | In-memory storage |
| Excel Processing | pandas + openpyxl | 2.3.3 + 3.1.5 | Data manipulation |
| Logging | Rich | 13.7.0 | Console logs |
| Monitoring | Langfuse | 2.18.0 | LLM observability |
| Frontend Framework | React | 18.2.0 | UI |
| Build Tool | Vite | 5.0.8 | Dev server & bundling |
| HTTP Client | Axios | 1.6.0 | API requests |

---

## Appendix B: Configuration Reference

### Backend Configuration (`app/core/config.py`)

```python
class Settings(BaseSettings):
    # API Keys
    openai_api_key: str = "XXXX"
    mistral_api_key: str = "XXXX"
    
    # Langfuse
    langfuse_public_key: str = "XXXX"
    langfuse_secret_key: str = "XXXX"
    langfuse_host: str = "https://cloud.langfuse.com"
    
    # Model Selection (MANUAL CHANGE REQUIRED)
    active_model: str = "openai"  # or "mistral"
    
    # Application
    upload_dir: str = "uploads"
    max_file_size_mb: int = 50
```

---

**End of Technical Document**
