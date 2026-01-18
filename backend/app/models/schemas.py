from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class FileUploadResponse(BaseModel):
    """Response for file upload"""
    filename: str
    tables_created: List[str]
    row_count: int
    status: str = "success"


class QuestionRequest(BaseModel):
    """Request for asking a question"""
    question: str
    model: Optional[str] = None  # Optional model override


class QuestionResponse(BaseModel):
    """Response for question answering"""
    question: str
    answer: str
    sql_queries: Optional[List[str]] = None
    data_used: Optional[List[str]] = None
    model: str
    timestamp: datetime = datetime.now()


class SchemaResponse(BaseModel):
    """Response for schema information"""
    tables: Dict[str, Any]
    total_tables: int
    total_rows: int


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None


class SQLQueryRequest(BaseModel):
    """Request for executing custom SQL query"""
    query: str


class SQLQueryResponse(BaseModel):
    """Response for SQL query execution"""
    query: str
    columns: List[str]
    rows: List[List[Any]]
    row_count: int
    status: str = "success"


class AgentExcelRequest(BaseModel):
    """Request for agent_excel endpoint
    
    Supports two modes:
    1. Custom GPT: openaiFileIdRefs with file objects containing download_link
    2. Direct API: excel_urls with direct URLs
    """
    query: str
    excel_urls: Optional[List[str]] = None
    openaiFileIdRefs: Optional[List[Any]] = None  # Can be dict or string


class AgentExcelLocalRequest(BaseModel):
    """Request for agent_excel_local endpoint
    
    Accepts local file paths on the server filesystem
    """
    query: str
    file_paths: List[str]


class AgentExcelResponse(BaseModel):
    """Response for agent_excel endpoint"""
    query: str
    answer: str
    sql_queries: Optional[List[str]] = None
    model: str
    files_processed: int
    tables_created: List[str]
    timestamp: datetime = datetime.now()
