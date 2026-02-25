from minipdf.utils import compress_pdf

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import os

console = Console()

def validate_quality(ctx: typer.Context, value: int):
    # ctx.params only contains arguments defined ABOVE this one
    if value != 80 and not ctx.params.get("lossy"):
        raise typer.BadParameter("Set --lossy to True to use custom quality.")
    return value


def format_bytes(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def compress(
    input: Path = typer.Argument(
        ..., help="PDF file to compess", exists=True, file_okay=True, dir_okay=False
    ),
    output: Path = typer.Option(
        "compressed.pdf", "--output", "-o", help="Filename for the compressed PDF"
    ),
    level: int = typer.Option(
        -1, 
        "--level", 
        min=-1, 
        max=9, 
        help=
        """
            Compression level: [0=None, 9=Max, -1=Standard]\n
            Higher values offer better compression but take more time
        """
    ),
    duplicate: bool = typer.Option(
        True, help="Whether to optimize duplicated elements (defaults to True)"
    ),
    lossy: bool = typer.Option(
        False, help="Whether to reduce quality of images"
    ),
    quality: int = typer.Option(
        80, "--quality", "-q", 
        min = 0,
        max = 100,
        callback=validate_quality,
        help=
        """
            Quality of images [0=Lowest, 100=Highest]\n
            Lower value offer better compression but with worse quality
        """
    )
):
    """
    Compress a PDF file
    """

    error = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Compressing PDF...", total=None)

        try:
            before = os.path.getsize(input)
            compress_pdf(input, output, duplicate, level, lossy, quality)
            after = os.path.getsize(output)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Compressed [cyan]{input}[/cyan] ([red]{format_bytes(before)}[/red]) to [cyan]{output}[/cyan] ([green]{format_bytes(after)}[/green])"
    )