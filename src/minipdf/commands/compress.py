from minipdf.utils import compress_pdf

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def compress(
    input: Path = typer.Argument(
        ..., help="PDF file to compess", exists=True, file_okay=True, dir_okay=False
    ),
    output: Path = typer.Option(
        "compressed.pdf", "--output", "-o", help="Filename for the compressed PDF"
    )
):
    """
    Compress a PDF while retaining full quality
    Can be CPU intensive
    """

    error = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Compressing PDF...", total=None)

        try:
            compress_pdf(input, output)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Compressed [cyan]{input}[/cyan] to [cyan]{output}[/cyan]"
    )