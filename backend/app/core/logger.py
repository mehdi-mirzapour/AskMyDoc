from rich.console import Console
from rich.logging import RichHandler
import logging

# Create Rich console
console = Console()

# Configure Rich logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, console=console)]
)

logger = logging.getLogger("askmydoc")
