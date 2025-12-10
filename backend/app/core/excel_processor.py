import pandas as pd
import sqlite3
from pathlib import Path
from typing import List, Dict, Any
from rich.progress import Progress, SpinnerColumn, TextColumn
from app.core.logger import logger, console


class ExcelProcessor:
    """Processes Excel files and loads them into SQLite database"""
    
    def __init__(self, db_path: str = ":memory:"):
        """Initialize with SQLite database
        
        Args:
            db_path: Path to SQLite database (default: in-memory)
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.tables: Dict[str, pd.DataFrame] = {}
        logger.info(f"[bold green]✓[/bold green] Initialized SQLite database: {db_path}", extra={"markup": True})
    
    def load_excel_file(self, file_path: Path) -> List[str]:
        """Load all sheets from an Excel file into SQLite
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            List of table names created
        """
        logger.info(f"[bold blue]📂 Loading Excel file:[/bold blue] {file_path.name}", extra={"markup": True})
        
        table_names = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Processing {file_path.name}...", total=None)
            
            try:
                # Read all sheets
                excel_file = pd.ExcelFile(file_path)
                
                for sheet_name in excel_file.sheet_names:
                    # Skip metadata sheets
                    if sheet_name.lower() in ['metadata', 'info']:
                        logger.info(f"  [dim]⊘ Skipping sheet: {sheet_name}[/dim]", extra={"markup": True})
                        continue
                    
                    # Read sheet
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    
                    # Create table name: filename_sheetname
                    # Sanitize names to remove dots and special characters
                    import re
                    def clean_name(n):
                        return re.sub(r'[^a-zA-Z0-9_]', '_', n)
                    
                    base_name = clean_name(file_path.stem)
                    clean_sheet = clean_name(sheet_name)
                    table_name = f"{base_name}_{clean_sheet}".lower()
                    
                    # Save to SQLite
                    df.to_sql(table_name, self.conn, if_exists='replace', index=False)
                    
                    # Store metadata
                    self.tables[table_name] = df
                    table_names.append(table_name)
                    
                    logger.info(
                        f"  [green]✓[/green] Loaded sheet '{sheet_name}' → table '{table_name}' "
                        f"({len(df)} rows, {len(df.columns)} columns)",
                        extra={"markup": True}
                    )
                
                progress.update(task, completed=True)
                logger.info(f"[bold green]✓ Completed loading {file_path.name}[/bold green]", extra={"markup": True})
                
            except Exception as e:
                logger.error(f"[bold red]✗ Error loading {file_path.name}:[/bold red] {e}", extra={"markup": True})
                raise
        
        return table_names
    
    def get_schema(self) -> Dict[str, Any]:
        """Get schema information for all loaded tables
        
        Returns:
            Dictionary with table schemas
        """
        schema = {}
        cursor = self.conn.cursor()
        
        for table_name in self.tables.keys():
            # Get column info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            schema[table_name] = {
                'columns': [col[1] for col in columns],
                'types': [col[2] for col in columns],
                'row_count': len(self.tables[table_name])
            }
        
        return schema
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results
        
        Args:
            query: SQL query string
            
        Returns:
            Query results as DataFrame
        """
        logger.info(f"[bold cyan]🔍 Executing SQL query:[/bold cyan]", extra={"markup": True})
        logger.info(f"[dim]{query}[/dim]", extra={"markup": True})
        
        try:
            result = pd.read_sql_query(query, self.conn)
            logger.info(f"[green]✓ Query returned {len(result)} rows[/green]", extra={"markup": True})
            return result
        except Exception as e:
            logger.error(f"[bold red]✗ Query error:[/bold red] {e}", extra={"markup": True})
            raise
    
    def get_table_preview(self, table_name: str, n: int = 5) -> pd.DataFrame:
        """Get preview of table
        
        Args:
            table_name: Name of table
            n: Number of rows to return
            
        Returns:
            First n rows of table
        """
        return self.execute_query(f"SELECT * FROM {table_name} LIMIT {n}")
    
    def close(self):
        """Close database connection"""
        self.conn.close()
        logger.info("[bold yellow]⊗ Closed database connection[/bold yellow]", extra={"markup": True})
