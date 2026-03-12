from minipdf.utils import image_to_pdf

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import List
from ..resolve import resolve_and_sort_files, SortChoice

console = Console()


def img2pdf(
    input_files: List[str] = typer.Argument(
        ...,
        help="List of image files to convert (in order)", metavar="FILES"
    ),
    output_file: Path = typer.Option(
        "images_merged.pdf", "--output", "-o", help="Filename of resulting PDF file", file_okay=True, dir_okay=False
    ),
    sort: SortChoice = typer.Option(
        SortChoice.none, 
        "--sort", 
        "-s",
        help="Sort the input files before converting"
    )
):
    """
    Convert a list of images and merge into a PDF file (in order)
    """

    resolved_files = resolve_and_sort_files(input_files, sort)

    error = None
    num_files = len(resolved_files)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Converting images...", total=None)



        try:
            image_to_pdf(resolved_files, output_file)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Converted [cyan]{num_files}[/cyan] images to [cyan]{output_file}[/cyan]"
    )
