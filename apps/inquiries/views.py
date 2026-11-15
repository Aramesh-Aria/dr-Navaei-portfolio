import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from .forms import InquiryForm

logger = logging.getLogger(__name__)

SENT = "inquiry-sent"


def notify(inquiry):
    """Email the clinic about a new Inquiry, only when an address is set.
    The Inquiry is already saved, so a failing email is logged, never raised."""
    recipient = getattr(settings, "INQUIRY_NOTIFICATION_EMAIL", "")
    if not recipient:
        return
    admin_url = settings.SITE_URL + reverse("admin:inquiries_inquiry_change", args=[inquiry.pk])
    lines = [
        f"نام: {inquiry.name}",
        f"تلفن: {inquiry.phone}",
        f"زمان مناسب برای تماس: {inquiry.preferred_contact_time or '-'}",
        "",
        inquiry.message or "(بدون پیام)",
        "",
        f"در بخش مدیریت: {admin_url}",
    ]
    try:
        send_mail(f"پیام تازه از سایت: {inquiry.name}", "\n".join(lines), None, [recipient])
    except Exception:
        logger.exception("Inquiry %s saved, but its notification email failed", inquiry.pk)


class ContactView(FormView):
    """`/contact/`: the clinic's phones first, then the Inquiry form.

    A sent form redirects back here (so a reload never sends it twice) and
    the confirmation shows once, carried by a one-time message. A filled
    honeypot (`website`) gets the same confirmation but is never saved.
    """

    template_name = "inquiries/contact.html"
    form_class = InquiryForm
    success_url = reverse_lazy("contact")

    def post(self, request, *args, **kwargs):
        # A filled honeypot is a bot: confirm before validating, so it learns
        # nothing from errors either, and save nothing.
        if request.POST.get("website", "").strip():
            return self.sent()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        notify(form.save())
        return self.sent()

    def sent(self):
        messages.success(self.request, SENT, extra_tags=SENT)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sent"] = any(m.message == SENT for m in messages.get_messages(self.request))
        return context
