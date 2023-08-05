# -*- coding: utf-8 -*-
__author__ = "Peter Gastinger"
__copyright__ = "Copyright 2020"
__credits__ = ["Peter Gastinger"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Peter Gastinger"
__email__ = "peter@secitec.net"
__status__ = "Production"

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_GET


@require_GET
def security_txt(request):
    lines = []

    for name in filter(lambda x: x.startswith("WELLKNOWN_SECURITY_"), dir(settings)):
        key = name.replace("WELLKNOWN_SECURITY_", "").lower().title()
        for value in getattr(settings, name):
            lines += [f"{key}: {value}"]
        lines += [""]

    return HttpResponse("\n".join(lines), content_type="text/plain")
