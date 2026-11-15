"""Resized WebP copies of the uploaded doctor photo (Stage 2 gate 7.3a).

The original upload is kept untouched; the site serves these copies instead,
so a several-MB phone photo is never the page's LCP image.

Which copies exist is remembered per process (`_made`): recorded when they are
written, or learned from one `exists()` the first time a name is rendered,
never asked again. Only "they exist" is remembered, so a worker that has not
seen a new upload's copies yet still finds them, and until then serves the
original. A replaced or cleared photo's copies are deleted and forgotten.
"""

from io import BytesIO
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

WIDTHS = (600, 1200)

_made = set()


def _key(storage, name):
    return (getattr(storage, "location", ""), name)


def check(field_file):
    """Decode the whole upload, as make_variants will; False if Pillow can't.

    Django's own check (`verify()`) passes a JPEG that is cut short, which
    would then fail at save with a 500."""
    try:
        field_file.seek(0)
        ImageOps.exif_transpose(Image.open(field_file)).load()
    except (OSError, SyntaxError, ValueError, Image.DecompressionBombError):
        return False
    finally:
        field_file.seek(0)
    return True


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
    _made.add(_key(storage, field_file.name))


def delete_variants(storage, name):
    """Delete the copies made for `name` (a photo that was replaced or cleared)."""
    _made.discard(_key(storage, name))
    for width in WIDTHS:
        variant = variant_name(name, width)
        if storage.exists(variant):
            storage.delete(variant)


def variant_url(field_file, width):
    """URL of an existing variant, or None if it was never made."""
    storage, key = field_file.storage, _key(field_file.storage, field_file.name)
    name = variant_name(field_file.name, width)
    if key not in _made:
        if not all(storage.exists(variant_name(field_file.name, w)) for w in WIDTHS):
            return None
        _made.add(key)
    return storage.url(name)
