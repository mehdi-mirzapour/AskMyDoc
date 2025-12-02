# AskMyDoc - AI-Powered Document Assistant

**Version:** 2.1.0  
**Status:** Stable (Pre-Production)

An intelligent document assistant that allows you to upload Excel files and ask natural language questions about them. Built with **FastAPI**, **LangChain**, **LangGraph**, and **React**.

![AskMyDoc UI](https://via.placeholder.com/800x400?text=AskMyDoc+Interface+Placeholder)

---

## 🚀 Features

- **🤖 AI-Powered Analysis**: Uses OpenAI GPT-4o-mini (default) or Mistral Large to understand your data.
- **📊 Multi-File Support**: Upload multiple Excel files (`.xlsx`, `.xls`) simultaneously.
- **💬 Natural Language Queries**: Ask questions in plain English (e.g., "Compare revenue between Q1 and Q2").
- **🔍 Deep Insights**: Supports aggregations, comparisons, rankings, and data quality checks.
- **⚡ Real-time Processing**: Fast in-memory SQLite database for instant query results.
- **🎨 Modern UI**: Beautiful React interface with animated landing page and chat experience.
- **🛠️ Robust Tooling**: Agent uses specialized tools for schema inspection, SQL execution, and data validation.
- **📈 Observability**: Integrated with Langfuse for tracking AI performance and costs.

---

## 📋 Prerequisites

- **Python** 3.9+
- **Node.js** 18+ and npm
- **OpenAI API Key** (Required)
- **Mistral API Key** (Optional)

---

## 🛠️ Installation

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment
# Create a .env file or edit app/core/config.py with your keys:
# OPENAI_API_KEY=sk-...
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

---

## 🏃 Running the Application

### Start Backend Server
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```
*Backend runs on `http://localhost:8000`*

### Start Frontend Client
```bash
cd frontend
npm run dev
```
*Frontend runs on `http://localhost:3000`*

---

## 📖 Usage Guide

1. **Open App**: Go to `http://localhost:3000`.
2. **Get Started**: Click the "Get Started" button on the landing page.
3. **Upload Files**: 
   - Click the 📎 icon in the chat bar.
   - Select one or more Excel files.
4. **Ask Questions**:
   - Type a question like "What is the total sales by region?"
   - Or click the 💡 icon to see sample questions.
5. **Analyze**: View the AI's answer and the generated SQL query used to get it.

### Example Questions
- *"Compute the total revenue per country across all files"*
- *"Which product has the highest average margin?"*
- *"Compare sales between Q1 and Q2"*
- *"List the top 5 customers by total spend"*
- *"Highlight any missing values or inconsistencies"*

---

## 🧪 Testing

The project includes a comprehensive integration test suite covering critical user journeys.

### Running Tests
```bash
cd backend
source venv/bin/activate
pytest tests/test_baseline.py -v
```

### Test Coverage
- ✅ **Aggregation**: Revenue by country
- ✅ **Comparison**: Q1 vs Q2 sales
- ✅ **Ranking**: Top customers
- ✅ **Data Quality**: Missing value detection
- ✅ **Complex Logic**: Highest margin product

---

## 🏗️ Architecture

- **Frontend**: React + Vite + Axios (Single Page Application)
- **Backend**: FastAPI (Async REST API)
- **Database**: SQLite (In-Memory)
- **AI Orchestration**: LangGraph (Stateful Agents)
- **LLM Integration**: LangChain (OpenAI/Mistral)

See [TECHNICAL_DOC.md](TECHNICAL_DOC.md) for detailed architecture, failure modes, and roadmap.

---

## 🔧 Configuration

**`backend/app/core/config.py`** manages settings. You can override these with environment variables.

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API Key | Required |
| `ACTIVE_MODEL` | Model to use (`openai` or `mistral`) | `openai` |
| `UPLOAD_DIR` | Directory for temp files | `uploads` |
| `MAX_FILE_SIZE_MB` | Max file size in MB | `50` |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
