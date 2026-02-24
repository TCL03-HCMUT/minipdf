from minipdf.utils import merge_pdfs

import typer
from pathlib import Path
from typing import List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# the merge sub‑tool should act as a group with a default action

console = Console()


def merge(
    files: List[Path] = typer.Argument(
        ...,
        help="List of PDF files to merge (in order)",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    output: Path = typer.Option(
        "merged.pdf", "--output", "-o", help="The filename for the resulting PDF"
    ),
):
    """
    Merge multiple PDF files into a single document.
    """
    if len(files) < 2:
        console.print("[yellow]Warning:[/yellow] You need at least 2 files to merge.")
        raise typer.Exit()

    error = None

    # Using 'Rich' to provide a professional CLI experience
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Merging PDFs...", total=None)

        try:
            merge_pdfs(files, output)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Merged {len(files)} files into [cyan]{output}[/cyan]"
    )
