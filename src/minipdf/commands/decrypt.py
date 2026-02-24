from minipdf.utils import decrypt_pdf

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def decrypt(
    input: Path = typer.Argument(
        ..., help="PDF file to decrypt", exists=True, file_okay=True, dir_okay=False
    ),
    output: Path = typer.Option(
        "decrypted.pdf", "--output", "-o", help="Filename for the decrypted PDF"
    ),
    password: str = typer.Option(
        None, "--password", "-p", help="Password to decrypt the PDF with (prompted if none is provided)"
    ),
):
    """
    Decrypt a PDF file with a password
    Show if decrypted password is user or owner
    """
    if password is None:
        password = typer.prompt("Password", hide_input=True)

    error = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Decrypting PDF...", total=None)

        try:
            user_pw_status = decrypt_pdf(input, output, password)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Success![/bold green] Decrypted [cyan]{input}[/cyan] ({"User" if user_pw_status else "Owner"} Password) to [cyan]{output}[/cyan]"
    )
