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
            auth_status = decrypt_pdf(input, output, password)
        except Exception as e:
            error = e

    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)

    match auth_status:
        case 1:
            status = "No password required"
        case 2:
            status = "Authenticated with the [bold green]user[/bold green] password"
        case 4:
            status = "Authenticated with the [bold green]owner[/bold green] password"
        case 6:
            status = "Authenticated, both [bold green]user[/bold green] and [bold green]owner[/bold green] passwords are equal"

    console.print(
        f"[bold green]Success![/bold green] Decrypted [cyan]{input}[/cyan] to [cyan]{output}[/cyan] ({status})"
    )
    
