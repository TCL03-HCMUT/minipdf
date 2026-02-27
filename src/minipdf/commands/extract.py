from minipdf.utils import extract_text

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def extract(
    input_file: Path = typer.Argument(
        ..., help="PDF file to extract text from", exists=True, file_okay=True, dir_okay=False
    ),
    output_file: Path = typer.Option(
        None, "--output", "-o", help="Filename for the output file",
        show_default="output.html if --html, else output.txt", file_okay=True, dir_okay=False
    ),
    html: bool = typer.Option(
        False, help="Whether to extract as HTML format"
    )
):
    """
    Extract all text from a PDF file

    WARNING: Results can be visually unappealing
    """
    if output_file is None:
        if html:
            output_file = Path("output.html")
        else:
            output_file = Path("output.txt")
    

    error = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Extracting text...", total=None)

        try:
            extract_text(input_file, output_file, html)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Extracted from [cyan]{input_file}[/cyan] to [cyan]{output_file}[/cyan]"
    )