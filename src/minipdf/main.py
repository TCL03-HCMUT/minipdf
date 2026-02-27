# src/pdfcli/main.py
import typer
from minipdf.commands.merge import merge
from minipdf.commands.split import split
from minipdf.commands.encrypt import encrypt
from minipdf.commands.decrypt import decrypt
from minipdf.commands.compress import compress
from minipdf.commands.extract import extract
from minipdf.commands.pdf2img import pdf2img
from minipdf.commands.img2pdf import img2pdf

app = typer.Typer(help="A mini PDF CLI tool")

app.command()(merge)
app.command()(split)
app.command()(encrypt)
app.command()(decrypt)
app.command()(compress)
app.command()(extract)
app.command()(pdf2img)
app.command()(img2pdf)

if __name__ == "__main__":
    app()
