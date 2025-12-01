from langchain_core.tools import tool
from typing import List
import pandas as pd
from app.core.logger import logger


# Global reference to processor (will be set by main app)
excel_processor = None


def set_processor(processor):
    """Set the global excel processor instance"""
    global excel_processor
    excel_processor = processor


@tool
def get_database_schema() -> str:
    """Get the schema of all available database tables including column names and types.
    Use this first to understand what data is available."""
    logger.info("[bold magenta]🔧 Tool called: get_database_schema[/bold magenta]", extra={"markup": True})
    
    schema = excel_processor.get_schema()
    
    result = "Available Tables:\n\n"
    for table_name, info in schema.items():
        result += f"Table: {table_name}\n"
        result += f"  Rows: {info['row_count']}\n"
        result += f"  Columns:\n"
        for col, dtype in zip(info['columns'], info['types']):
            result += f"    - {col} ({dtype})\n"
        result += "\n"
    
    logger.info(f"[green]✓ Returned schema for {len(schema)} tables[/green]", extra={"markup": True})
    return result


@tool
def execute_sql_query(query: str) -> str:
    """Execute a SQL query on the database and return results.
    
    Args:
        query: SQL query to execute
        
    Returns:
        Query results as formatted string
    """
    logger.info(f"[bold magenta]🔧 Tool called: execute_sql_query[/bold magenta]", extra={"markup": True})
    
    try:
        result_df = excel_processor.execute_query(query)
        
        if result_df.empty:
            return "Query returned no results."
        
        # Format results
        result_str = result_df.to_string(index=False, max_rows=100)
        logger.info(f"[green]✓ Query executed successfully, {len(result_df)} rows returned[/green]", extra={"markup": True})
        return result_str
        
    except Exception as e:
        error_msg = f"Error executing query: {str(e)}"
        logger.error(f"[red]✗ {error_msg}[/red]", extra={"markup": True})
        return error_msg


@tool
def preview_table(table_name: str, num_rows: int = 5) -> str:
    """Preview the first few rows of a table.
    
    Args:
        table_name: Name of the table to preview
        num_rows: Number of rows to show (default: 5)
        
    Returns:
        Preview of table
    """
    logger.info(f"[bold magenta]🔧 Tool called: preview_table ({table_name})[/bold magenta]", extra={"markup": True})
    
    try:
        df = excel_processor.get_table_preview(table_name, num_rows)
        result = df.to_string(index=False)
        logger.info(f"[green]✓ Preview retrieved[/green]", extra={"markup": True})
        return result
    except Exception as e:
        error_msg = f"Error previewing table: {str(e)}"
        logger.error(f"[red]✗ {error_msg}[/red]", extra={"markup": True})
        return error_msg


@tool
def check_missing_values() -> str:
    """Check for missing values (NULL/NaN) across all tables.
    
    Returns:
        Report of missing values
    """
    logger.info("[bold magenta]🔧 Tool called: check_missing_values[/bold magenta]", extra={"markup": True})
    
    report = "Missing Values Report:\n\n"
    
    for table_name, df in excel_processor.tables.items():
        missing = df.isnull().sum()
        missing_cols = missing[missing > 0]
        
        if not missing_cols.empty:
            report += f"Table: {table_name}\n"
            for col, count in missing_cols.items():
                report += f"  - {col}: {count} missing values\n"
            report += "\n"
    
    if report == "Missing Values Report:\n\n":
        report += "No missing values found in any table."
    
    logger.info("[green]✓ Missing values check completed[/green]", extra={"markup": True})
    return report


# List of all tools
tools = [
    get_database_schema,
    execute_sql_query,
    preview_table,
    check_missing_values
]
