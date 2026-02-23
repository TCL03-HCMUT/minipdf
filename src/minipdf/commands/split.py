from minipdf.utils import split_pdf

import typer
from pathlib import Path
from typing import List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn



console = Console()


def split(
    input: Path = typer.Argument(
        ...,
        help="PDF file to split",
        exists=True, 
        file_okay=True, 
        dir_okay=False
    ),
    output: Path = typer.Argument(
        ...,
        help="Directory of output",
        file_okay=False, 
        dir_okay=True
    )
):
    """
    Split one PDF file into separate pages
    """
    paths = []
    error = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Splitting PDF...", total=None)
        
        try:
            paths = split_pdf(input, output)
        except Exception as e:
            error = e
    
    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)
    
    console.print(f"[bold green]Success![/bold green] Splitted into {len(paths)} pages")
    