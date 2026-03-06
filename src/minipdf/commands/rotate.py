from minipdf.utils import rotate_pdf

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import List, Optional

console = Console()


def validate_pages(value: str):
    if value is None:
        return []
    
    try:
        # Split, strip, and convert to int
        return [int(item.strip()) for item in value.split(",")]
    except ValueError:
        raise typer.BadParameter("Only comma-separated integers are allowed (e.g., '1,2,3').")


def rotate(
    input_file: Path = typer.Argument(
        ..., help="PDF file to rotate", exists=True, file_okay=True, dir_okay=False
    ),
    output_file: Path = typer.Option(
        "rotated.pdf", "--output", "-o", help="Filename for the rotated PDF", file_okay=True, dir_okay=False
    ),
    angle: int = typer.Option(
        90, "--angle", "-a", help="The angle to rotate the PDF file by (must be a multiple of 90)"
    ),
    pages: str = typer.Option(
        None,
        "--pages",
        "-p",
        callback=validate_pages,
        metavar="INT,INT,...",
        help="List of comma separated page numbers to rotate",
    )
):
    """
    Rotate a PDF file by an angle that is a multiple of 90. If a list of pages is passed, only those pages are rotated
    """
    error = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Rotating PDF...", total=None)

        try:
            rotate_pdf(input_file, output_file, angle, pages)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Rotated [cyan]{input_file}[/cyan] to [cyan]{output_file}[/cyan]"
    )
