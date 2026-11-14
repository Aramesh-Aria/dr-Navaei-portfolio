from django.views.generic import TemplateView


class ShellPreviewView(TemplateView):
    """TEMPORARY (Stage 3): renders only the shared shell so it can be
    verified. Stage 4 replaces it with the real home page."""

    template_name = "core/shell_preview.html"
