from minipdf.utils import pdf_to_docx

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import List
from ..resolve import resolve_and_sort_files, SortChoice
import os

console = Console()


def pdf2docx(
    input_files: List[str] = typer.Argument(
        ...,
        help="List of PDF files to convert", metavar="FILES"
    ),
    output_dir: Path = typer.Option(
        ".", "--output-dir", help="Directory of output", file_okay=False, dir_okay=True
    ),
    ocr_tessdata: Path = typer.Option(
        None, "--ocr", help="Directory of Tesseract's language support folder for better conversion with OCR", dir_okay=True, file_okay=False
    )
):
    """
    Convert a list of PDF file into respective Markdown files
    """

    resolved_files = resolve_and_sort_files(input_files, SortChoice.none)

    error = None
    num_files = len(resolved_files)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Converting files...", total=None)



        try:
            os.environ["TESSDATA_PREFIX"] = str(ocr_tessdata)
            pdf_to_docx(resolved_files, output_dir)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Converted [cyan]{num_files}[/cyan] files"
    )
