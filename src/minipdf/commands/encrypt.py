from minipdf.utils import encrypt_pdf

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def encrypt(
    input: Path = typer.Argument(
        ...,
        help="PDF file to encrypt",
        exists=True,
        file_okay=True,
        dir_okay=False
    ),
    output: Path = typer.Option(
        "encrypted.pdf",
        "--output", "-o",
        help="Filename for the encrypted PDF"
    ),
    password: str = typer.Option(
        None,
        "--password", "-p",
        help="Password to encrypt the PDF with"
    ),
    owner_password: str = typer.Option(
        None,
        "--owner-password", "-op",
        help="Owner password (optional for document permissions)"
    )
):
    """
    Encrypt a PDF file with a password.
    """
    if password is None:
        password = typer.prompt("Password", hide_input=True)
    
    error = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Encrypting PDF...", total=None)
        
        try:
            encrypt_pdf(input, output, password, owner_password)
        except Exception as e:
            error = e
    
    if error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1)
    
    console.print(f"[bold green]Success![/bold green] Encrypted [cyan]{input}[/cyan] to [cyan]{output}[/cyan]")