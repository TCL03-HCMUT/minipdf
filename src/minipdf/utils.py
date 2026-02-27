import sys, pymupdf, io
from pathlib import Path
from typing import List, Optional
from PIL import Image


def validate_pdf_no_encryption_check(file_path: Path) -> bool:
    """
    Check if a file exists and if it's a valid PDF structure
    """
    if not file_path.exists():
        return False
    try:
        with pymupdf.open(file_path) as doc:
            return doc.is_pdf
    except Exception:
        return False


def validate_pdf(file_path: Path) -> bool:
    """
    Check if a file exists, is valid, and is NOT encrypted
    """
    if not file_path.exists():
        return False
    try:
        with pymupdf.open(file_path) as doc:
            return doc.is_pdf and not doc.is_encrypted
    except Exception:
        return False


def validate(file_path: Path):
    if not validate_pdf(file_path):
        raise ValueError(f"Invalid/encrypted file: {file_path}")


def merge_pdfs(input_paths: List[Path], output_path: Path) -> None:
    """
    Merge several PDF files into one
    """
    result = pymupdf.open()

    for path in input_paths:
        if not validate_pdf(path):
            print(f"Skipping invalid/encrypted file: {path}", file=sys.stderr)
            continue

        with pymupdf.open(path) as src:
            result.insert_pdf(src)

    if len(result) > 0:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result.save(output_path)

    result.close()


def split_pdf(input_path: Path, output_dir: Path) -> List[Path]:
    """
    Split a PDF into individual pages
    """
    validate(input_path)
    created_files = []
    output_dir.mkdir(parents=True, exist_ok=True)

    with pymupdf.open(input_path) as src:
        for page_num in range(len(src)):
            doc_page = pymupdf.open()
            doc_page.insert_pdf(src, from_page=page_num, to_page=page_num)

            filename = output_dir / f"{input_path.stem}_page_{page_num + 1}.pdf"
            doc_page.save(filename)
            doc_page.close()
            created_files.append(filename)

    return created_files


def encrypt_pdf(
    input_path: Path,
    output_path: Path,
    user_password: str,
    owner_password: str | None = None,
) -> None:
    """
    Encrypt a PDF file using AES-256
    """
    validate(input_path)

    with pymupdf.open(input_path) as doc:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(
            output_path,
            encryption=pymupdf.PDF_ENCRYPT_AES_256, #type:ignore
            user_pw=user_password,
            owner_pw=owner_password if owner_password else user_password,
            permissions=pymupdf.PDF_PERM_ACCESSIBILITY, #type:ignore
        )


def decrypt_pdf(input_path: Path, output_path: Path, password: str) -> int:
    """
    Decrypt a PDF file using the provided password
    """

    if not validate_pdf_no_encryption_check(input_path):
        raise ValueError(f"Invalid file: {input_path}")

    with pymupdf.open(input_path) as doc:
        if doc.is_encrypted:

            auth_status = doc.authenticate(password)
            if not auth_status:
                raise RuntimeError("Incorrect password!")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path)

        # Returns True if authenticated as user, False otherwise
        return auth_status


def compress_pdf(
    input_path: Path,
    output_path: Path,
) -> None:
    """
    Compress a PDF file by optimizing resources and garbage collecting
    """
    validate(input_path)

    with pymupdf.open(input_path) as doc:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path, garbage=4, deflate=True, clean=True)


def extract_text(input_path: Path, output_path: Path, html: bool = False):
    """
    Extract text from PDF file to a txt/HTML file
    """
    validate(input_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not html:
        with pymupdf.open(input_path) as doc:
            text = chr(12).join([page.get_text() for page in doc])  # type: ignore

        Path(output_path).write_bytes(text.encode())
    else:
        with pymupdf.open(input_path) as doc:
            html_content = "".join(page.get_text("html") for page in doc)  # type: ignore

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)


def pdf2image(input_path: Path, output_dir: Path, format: str = "png"):
    """
    Convert a PDF file to a list of images, one for each page
    If the GIF format is used, one GIF file is proudced instead, with each page as one frame
    """
    validate(input_path)

    output_dir.mkdir(parents=True, exist_ok=True)

    with pymupdf.open(input_path) as doc:
        if format != "gif":
            for i, page in enumerate(doc): #type:ignore
                pix = page.get_pixmap()  # Render page to an image
                pix.save(output_dir / f"{input_path.name}_page_{i}.{format}")
        else:
            images = []
            for page in doc:
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                images.append(Image.open(io.BytesIO(img_bytes)))

            if images:
                images[0].save(
                    output_dir / f"{input_path.stem}.gif",
                    save_all=True,
                    append_images=images[1:],
                    duration=1000,  # Duration of each frame in ms
                    loop=0,  # 0 means infinite loop
                )


def image2pdf(input_images: List[Path], output_path: Path):
    """
    Convert a list of images into a PDF file (in order)
    """

    images = [Image.open(input_image).convert("RGB") for input_image in input_images]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    images[0].save(output_path, save_all=True, append_images=images[1:])