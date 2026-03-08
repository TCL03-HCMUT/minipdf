from minipdf.utils import show_metadata

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def metadata(
    input_file: Path = typer.Argument(
        ...,
        help="PDF file to extract metadata from", exists=True, file_okay=True, dir_okay=False,
    )
):
    """
    Print the metadata of a PDF file
    """

    error = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Extracting metadata...", total=None)

        try:
            meta = show_metadata(input_file)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold]Metadata of [cyan]{input_file}[/cyan][/bold]:\n{meta}")
