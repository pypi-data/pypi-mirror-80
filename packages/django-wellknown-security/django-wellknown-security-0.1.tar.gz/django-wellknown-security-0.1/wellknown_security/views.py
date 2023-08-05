from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_GET


@require_GET
def security_txt(request):
    lines = [
        "Contact: " + settings.WELLKNOWN_SECURITY_CONTACT,
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
