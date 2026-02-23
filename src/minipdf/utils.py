import sys
from pathlib import Path
from typing import List, Optional
from pypdf import PdfWriter, PdfReader
from pypdf.errors import PdfReadError
from pypdf import PasswordType

def validate_pdf_no_encryption_check(file_path : Path) -> bool:
    """Check if a file exists and if it's valid (not including encryption check)"""

    if not file_path.exists():
        return False
    
    try:
        reader = PdfReader(file_path)

        return True
    except PdfReadError:
        return False


def validate_pdf(file_path : Path) -> bool:
    """Check if a file exists and if it's valid"""
    if not validate_pdf_no_encryption_check(file_path):
        return False
    
    reader = PdfReader(file_path)
    is_encrypted = reader.is_encrypted
    reader.close()
    return not is_encrypted


def merge_pdfs(input_paths : List[Path], output_path : Path) -> None:
    """
    Merge several PDF files into one file
    Handle basic validation
    """

    writer = PdfWriter()

    for path in input_paths:
        if not validate_pdf(path):
            print(f"Skipping invalid/encrypted files: {path}", file=sys.stderr)
            continue

        try:
            writer.append(path)
        except Exception as e:
            writer.close()
            raise RuntimeError(f"Failed to append {path.name}: {e}")
    

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        writer.write(f)
    
    writer.close()


def split_pdf(input_path : Path, output_dir : Path) -> List[Path]:
    """
    Split a PDF into individual pages.
    Returns a list of file paths.
    """

    if not validate_pdf(input_path):
        raise ValueError(f"Invalid/encrypted file: {input_path}")
    

    reader = PdfReader(input_path)
    created_files = []

    output_dir.mkdir(parents=True, exist_ok=True)

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)

        filename = output_dir / f"{input_path.name}_page_{i + 1}.pdf"

        with open(filename, "wb") as f:
            writer.write(f)
        
        writer.close()

        created_files.append(filename)
    
    reader.close()
    return created_files


def encrypt_pdf(input_path : Path, output_path : Path, user_password : str, owner_password : str | None = None) -> None:
    """
    Encrypt a PDF file using the password provided
    An owner password can be optionally passed in
    """
    if not validate_pdf_no_encryption_check(input_path):
        raise ValueError(f"Invalid file: {input_path}")
    
    reader = PdfReader(input_path)
    writer = PdfWriter(clone_from=reader)
    if not owner_password:
        writer.encrypt(user_password, algorithm="AES-256")
    else:
        writer.encrypt(user_password, owner_password, algorithm="AES-256")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        writer.write(f)
    
    writer.close()
    reader.close()


def decrypt_pdf(input_path : Path, output_path : Path, password : str) -> bool:
    """
    Decrypt a PDF file using the provided password
    Returns true if the User Password is decoded, False if the Owner Password is decoded (only for internal use)
    """
    if not validate_pdf_no_encryption_check(input_path):
        raise ValueError(f"Invalid file: {input_path}")
    
    reader = PdfReader(input_path)

    if reader.is_encrypted:
        status = reader.decrypt(password)

        if status == PasswordType.NOT_DECRYPTED:

            reader.close()
            raise RuntimeError("Incorrect password!")
    
    writer = PdfWriter(clone_from=reader)
    with open(output_path, "wb") as f:
        writer.write(f)
    writer.close()
    reader.close()

    return status == PasswordType.USER_PASSWORD