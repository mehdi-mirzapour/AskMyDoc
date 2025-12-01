# AskMyDoc - AI-Powered Document Assistant

An intelligent document assistant that allows you to upload Excel files and ask natural language questions about them. Built with FastAPI, LangChain, LangGraph, and React.

## 🚀 Features

- **Multi-File Upload**: Upload multiple Excel files simultaneously
- **Natural Language Queries**: Ask questions in plain English
- **AI-Powered Analysis**: Uses LangChain & LangGraph with OpenAI or Mistral
- **SQLite Database**: Efficient data querying with SQL
- **Beautiful UI**: Modern React interface with drag-and-drop upload
- **Rich Logging**: Detailed console logs with Rich library
- **Langfuse Integration**: Track and monitor AI agent performance

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+ and npm (for frontend)
- OpenAI API key or Mistral API key

## 🛠️ Installation

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys:**
   
   Edit `app/core/config.py` and replace `XXXX` with your actual API keys:
   ```python
   openai_api_key: str = "your-openai-key"
   mistral_api_key: str = "your-mistral-key"
   langfuse_public_key: str = "your-langfuse-public-key"
   langfuse_secret_key: str = "your-langfuse-secret-key"
   ```

5. **Change active model (optional):**
   
   In `app/core/config.py`, change the `active_model` setting:
   ```python
   active_model: str = "openai"  # or "mistral"
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## 🏃 Running the Application

### Start Backend Server

```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:3000`

## 📖 Usage

1. **Open your browser** to `http://localhost:3000`

2. **Upload Excel files:**
   - Drag and drop files or click to browse
   - Supports `.xlsx` and `.xls` formats
   - Multiple files can be uploaded at once

3. **Ask questions:**
   - Type your question in the chat interface
   - Examples:
     - "Compute the total revenue per country across all files"
     - "Which product has the highest average margin?"
     - "List the top 5 customers by total spend"
     - "Highlight any missing values or inconsistencies"

4. **View results:**
   - AI-generated answers appear in the chat
   - SQL queries used are shown in expandable sections
   - Model information is displayed for each response

## 🧪 Testing

Test files are provided in the `tests/excels/` directory:

```bash
cd backend
source venv/bin/activate

# Upload the test files via the UI and try these questions:
```

**Test Questions:**
1. Compute the total revenue per country across all files
2. Which product has the highest average margin?
3. Compare sales between Q1 and Q2
4. List the top 5 customers by total spend
5. Highlight any missing values or inconsistencies

## 📁 Project Structure

```
AskMyDoc/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── api/                 # API endpoints
│   │   ├── core/                # Core functionality
│   │   │   ├── config.py        # Configuration
│   │   │   ├── excel_processor.py  # Excel → SQLite
│   │   │   └── logger.py        # Rich logging
│   │   ├── agents/              # LangGraph agents
│   │   │   ├── document_agent.py
│   │   │   └── tools.py         # LangChain tools
│   │   └── models/              # Pydantic schemas
│   ├── requirements.txt
│   └── uploads/                 # Uploaded files
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/            # API client
│   │   ├── App.jsx              # Main component
│   │   └── main.jsx             # Entry point
│   └── package.json
└── tests/
    └── excels/                  # Test Excel files
```

## 🔧 Configuration

### Switching AI Models

Edit `backend/app/core/config.py`:

```python
active_model: str = "openai"  # Change to "mistral" for Mistral
```

Restart the backend server for changes to take effect.

### Langfuse Integration

To enable Langfuse tracking, update your keys in `backend/app/core/config.py`:

```python
langfuse_public_key: str = "pk-..."
langfuse_secret_key: str = "sk-..."
langfuse_host: str = "https://cloud.langfuse.com"
```

## 🐛 Troubleshooting

**Backend won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that API keys are configured correctly
- Verify Python version is 3.9+

**Frontend won't start:**
- Run `npm install` to install dependencies
- Ensure Node.js 18+ is installed
- Check that backend is running on port 8000

**Upload fails:**
- Verify file is `.xlsx` or `.xls` format
- Check file size is under 50MB
- Ensure backend is running

**No answer returned:**
- Check API keys are valid
- Ensure files were uploaded successfully
- View backend logs for errors

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for any purpose.

## 🙏 Acknowledgments

- FastAPI
- LangChain & LangGraph
- OpenAI & Mistral AI
- React
- Rich (Python logging)
- Langfuse
