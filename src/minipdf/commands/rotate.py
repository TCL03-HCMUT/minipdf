from minipdf.utils import rotate_pdf

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


import typer

def validate_pages(value: str):
    if not value:
        return []
    
    pages = set() # avoid duplicates
    
    try:
        parts = [item.strip() for item in value.split(",")]
        
        for part in parts:
            if "-" in part:
                # handling ranges
                start_str, end_str = part.split("-")
                start, end = int(start_str), int(end_str)
                
                if start > end:
                    raise typer.BadParameter(f"Invalid range: {part}. Start must be less than end.")
                
                # Add all numbers in the range (inclusive)
                pages.update(range(start, end + 1))
            else:
                pages.add(int(part))
                
        return sorted(list(pages))
        
    except ValueError:
        raise typer.BadParameter("Format must be integers or ranges (e.g. '1, 3-6, 9')")


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
        metavar="INT,INT-INT,...",
        help="List of comma separated page numbers/ranges to rotate (e.g. '1, 3-6, 9')",
    )
):
    """
    Rotate a PDF file by an angle that is a multiple of 90. Positive angle value indicates clockwise rotation, negative indicates otherwise.
    
    If a list of pages is passed, only those pages are rotated.
    """
    error = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Rotating PDF...", total=None)

        try:
            rotate_pdf(input_file, output_file, angle, pages) # type:ignore
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Rotated [cyan]{input_file}[/cyan] to [cyan]{output_file}[/cyan]"
    )
