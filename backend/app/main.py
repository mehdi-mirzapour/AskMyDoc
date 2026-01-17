from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.excel_processor import ExcelProcessor
from app.agents import tools
from app.api import upload, query, agent_excel, agent_upload, storage
from app.core.logger import logger, console
from app.core.config import get_settings
from rich.panel import Panel

# Initialize FastAPI app
app = FastAPI(
    title="AskMyDoc API",
    description="AI-powered document assistant for Excel files",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
excel_processor = ExcelProcessor()
tools.set_processor(excel_processor)

# Set processors in routers
upload.set_excel_processor(excel_processor)
query.set_excel_processor(excel_processor)
agent_excel.set_excel_processor(excel_processor)
agent_upload.set_excel_processor(excel_processor)

# Include routers
app.include_router(upload.router)
app.include_router(query.router)
app.include_router(agent_excel.router)
app.include_router(agent_upload.router)
app.include_router(storage.router)


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    console.print(Panel.fit(
        "[bold green]🚀 AskMyDoc API Server Started[/bold green]\n\n"
        f"[cyan]Active Model:[/cyan] {get_settings().active_model}\n"
        "[cyan]Status:[/cyan] Ready to accept requests\n"
        "[dim]Upload Excel files and ask questions![/dim]",
        border_style="green"
    ))


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    excel_processor.close()
    logger.info("[yellow]Server shutting down...[/yellow]", extra={"markup": True})


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AskMyDoc API",
        "version": "1.0.0",
        "status": "running",
        "active_model": get_settings().active_model
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "agent": "ready"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5888)
