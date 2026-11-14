"""Resized WebP copies of the uploaded doctor photo (Stage 2 gate 7.3a).

The original upload is kept untouched; the site serves these copies instead,
so a several-MB phone photo is never the page's LCP image.
"""

from io import BytesIO
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

WIDTHS = (600, 1200)


def variant_name(name, width):
    """doctor/portrait.jpg → doctor/portrait-1200.webp"""
    path = PurePosixPath(name)
    return str(path.with_name(f"{path.stem}-{width}.webp"))


def make_variants(field_file):
    """Write one WebP per width beside the original. Never enlarges."""
    storage = field_file.storage
    field_file.open("rb")
    try:
        image = ImageOps.exif_transpose(Image.open(field_file))
        image.load()
    finally:
        field_file.close()
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")
    for width in WIDTHS:
        copy = image.copy()
        if copy.width > width:
            copy = copy.resize((width, round(copy.height * width / copy.width)), Image.LANCZOS)
        buffer = BytesIO()
        copy.save(buffer, "WEBP", quality=82, method=6)
        name = variant_name(field_file.name, width)
        if storage.exists(name):
            storage.delete(name)
        storage.save(name, ContentFile(buffer.getvalue()))


def variant_url(field_file, width):
    """URL of an existing variant, or None if it was never made."""
    name = variant_name(field_file.name, width)
    if field_file.storage.exists(name):
        return field_file.storage.url(name)
    return None
