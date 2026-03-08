from minipdf.utils import office_to_pdf

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import List


console = Console()


def office2pdf(
    input_files: List[Path] = typer.Argument(
        ...,
        help="List of MS Office files to convert (in order)", exists=True, file_okay=True, dir_okay=False,
    ),
    output_dir: Path = typer.Option(
        ".", "--output-dir", help="Filename of resulting PDF file", file_okay=False, dir_okay=True
    )
):
    """
    Convert a list of MS Office files into respective PDF files

    Requires MS Office or LibreOffice to be installed on the system
    """

    error = None
    num_files = len(input_files)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Converting files...", total=None)

        try:
            office_to_pdf(input_files, output_dir)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Converted [cyan]{num_files}[/cyan] files to PDF"
    )
