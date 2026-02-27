from minipdf.utils import image2pdf

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import List


console = Console()


def img2pdf(
    input_files: List[Path] = typer.Argument(
        ...,
        help="List of PDF files to convert (in order)", exists=True, file_okay=True, dir_okay=False,
    ),
    output_file: Path = typer.Option(
        "images_merged.pdf", "--output", "-o", help="Filename of resulting PDF file", file_okay=True, dir_okay=False
    )
):
    """
    Convert a list of images and merge into a PDF file (in order)
    """

    error = None
    num_files = len(input_files)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Converting images...", total=None)

        try:
            image2pdf(input_files, output_file)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Converted [cyan]{num_files}[/cyan] images to [cyan]{output_file}[/cyan]"
    )