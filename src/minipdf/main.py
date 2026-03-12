import typer
from minipdf.commands.core import merge, split, extract, rotate
from minipdf.commands.security import encrypt, decrypt
from minipdf.commands.conversion import img2pdf, pdf2img, office2pdf, pdf2md
from minipdf.commands.optimization import compress, metadata

app = typer.Typer(help="A mini PDF CLI tool")

# Create command groups
core_app = typer.Typer(help="Core PDF operations")
core_app.command()(merge)
core_app.command()(split)
core_app.command()(extract)
core_app.command()(rotate)

security_app = typer.Typer(help="PDF security operations")
security_app.command()(encrypt)
security_app.command()(decrypt)

conversion_app = typer.Typer(help="PDF format conversions")
conversion_app.command()(img2pdf)
conversion_app.command()(pdf2img)
conversion_app.command()(office2pdf)
conversion_app.command()(pdf2md)

optimization_app = typer.Typer(help="PDF optimization operations")
optimization_app.command()(compress)
optimization_app.command()(metadata)

# Add command groups to main app
app.add_typer(core_app, name="core", help="Basic PDF operations (merge, split, extract, rotate, etc.)")
app.add_typer(security_app, name="secure", help="Encryption, decryption")
app.add_typer(conversion_app, name="convert", help="Format conversions (images, MS Office documents, etc.)")
app.add_typer(optimization_app, name="optimize", help="Optimization (compress, metadata, etc.)")

if __name__ == "__main__":
    app()
