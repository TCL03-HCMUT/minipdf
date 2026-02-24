# src/pdfcli/main.py
import typer
from minipdf.commands.merge import merge
from minipdf.commands.split import split
from minipdf.commands.encrypt import encrypt
from minipdf.commands.decrypt import decrypt
from minipdf.commands.compress import compress

app = typer.Typer(help="A mini PDF CLI tool")

app.command()(merge)
app.command()(split)
app.command()(encrypt)
app.command()(decrypt)
app.command()(compress)

if __name__ == "__main__":
    app()
