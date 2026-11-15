from whitenoise.storage import CompressedManifestStaticFilesStorage

# Third-party paths that may reference files their package doesn't ship.
VENDOR_PREFIXES = ("admin/", "vendor/")


class StaticFilesStorage(CompressedManifestStaticFilesStorage):
    """Hashed, compressed static files, strict about the site's own references.

    With DEBUG off, `{% static %}` links the hashed name (cached for a year)
    and a path missing from the manifest is an error, so a forgotten
    `collectstatic` fails loudly instead of shipping a broken link. A vendor
    path that can't be hashed is served under its plain name instead.
    """

    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:  # Django's "file could not be found"
            if name.startswith(VENDOR_PREFIXES):
                return name
            raise

    def stored_name(self, name):
        try:
            return super().stored_name(name)
        except ValueError:  # Django's "missing staticfiles manifest entry"
            if name.startswith(VENDOR_PREFIXES):
                return name
            raise
