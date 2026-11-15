from django.utils.cache import patch_cache_control


class RevalidateHtmlMiddleware:
    """Make browsers revalidate every HTML page (owner decision, Stage 2 gate).

    Static files have content-hashed names, so a changed CSS or JS file gets a
    new URL. `no-cache` (not `no-store`) makes sure the page that links the new
    URL is always fetched fresh, while keeping the back/forward cache usable.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.get("Content-Type", "").startswith("text/html"):
            patch_cache_control(response, no_cache=True)
        return response
