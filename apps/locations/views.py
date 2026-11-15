from django.views.generic import TemplateView


class LocationsView(TemplateView):
    """`/locations/`: every Clinic Location with all its fields. The
    locations themselves come from the site context processor."""

    template_name = "locations/list.html"
