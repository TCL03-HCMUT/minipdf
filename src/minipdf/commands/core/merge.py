from minipdf.utils import merge_pdfs

import typer
from pathlib import Path
from typing import List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from ..resolve import resolve_and_sort_files, SortChoice

console = Console()


def merge(
    input_files: List[str] = typer.Argument(
        ...,
        help="List of PDF files to merge (in order)", metavar="FILES"
    ),
    output_file: Path = typer.Option(
        "merged.pdf", "--output", "-o", help="The filename for the resulting PDF", file_okay=True, dir_okay=False
    ),
    sort: SortChoice = typer.Option(
        SortChoice.none, 
        "--sort", 
        "-s",
        help="Sort the input files before converting"
    )
):
    """
    Merge multiple PDF files into a single document
    """
    

    resolved_files = resolve_and_sort_files(input_files, sort)

    if len(resolved_files) < 2:
        console.print("[yellow]Warning:[/yellow] You need at least 2 files to merge.")
        raise typer.Exit()

    error = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Merging PDFs...", total=None)

        try:
            merge_pdfs(resolved_files, output_file)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Merged [cyan]{len(input_files)}[/cyan] files into [cyan]{output_file}[/cyan]"
    )
