from minipdf.utils import pdf2image

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


console = Console()


def pdf2img(
    input_file: Path = typer.Argument(
        ..., help="PDF file to convert", exists=True, file_okay=True, dir_okay=False
    ),
    output_dir: Path = typer.Option(
        "./", "--output-dir", help="Directory of output", file_okay=False, dir_okay=True
    ),
    format: str = typer.Option(
        "png", "--format", "-f", help="Format of resulting files"
    )
):
    """
    Convert a PDF file to a list of images, one for each page

    If the GIF format is used, one GIF file is proudced instead, with each page as one frame
    """

    error = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Converting PDF...", total=None)

        try:
            pdf2image(input_file, output_dir, format.strip().lower())
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(f"[bold green]Success![/bold green] PDF file has been converted into {"GIF" if format.lower().strip() == "gif" else "images"}")