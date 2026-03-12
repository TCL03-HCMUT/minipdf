import typer
import glob
from enum import Enum
from typing import List
from pathlib import Path
from rich.console import Console

console = Console()

# Assume rich console is already imported

class SortChoice(str, Enum):
    none = "none"
    filename = "filename"
    date = "date"
    size = "size"

def resolve_and_sort_files(patterns: List[str], sort: SortChoice) -> List[Path]:
    """
    Takes a list of string patterns (including wildcards), expands them, 
    validates them as files, deduplicates, and sorts them.
    """
    resolved_files: List[Path] = []
    
    for pattern in patterns:
        matches = glob.glob(pattern)
        
        if not matches:
            console.print(f"[bold yellow]Warning:[/bold yellow] No files matched the pattern: '{pattern}'")
            continue
            
        for match in matches:
            p = Path(match)
            if p.is_file():
                resolved_files.append(p)
            elif p.is_dir():
                console.print(f"[bold yellow]Warning:[/bold yellow] Skipping directory: {p}")

    # Deduplicate while preserving order
    resolved_files = list(dict.fromkeys(resolved_files))

    if not resolved_files:
        console.print("[bold red]Error:[/bold red] No valid files provided to process.")
        raise typer.Exit(code=1)

    # Apply Sorting Logic
    if sort == SortChoice.filename:
        resolved_files = sorted(resolved_files, key=lambda f: f.name)
    elif sort == SortChoice.date:
        resolved_files = sorted(resolved_files, key=lambda f: f.stat().st_mtime)
    elif sort == SortChoice.size:
        resolved_files = sorted(resolved_files, key=lambda f: f.stat().st_size)

    return resolved_files