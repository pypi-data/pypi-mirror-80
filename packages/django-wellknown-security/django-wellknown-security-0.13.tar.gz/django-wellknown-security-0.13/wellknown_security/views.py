from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_GET


@require_GET
def security_txt(request):
    lines = []

    for name in filter(lambda x: x.startswith('WELLKNOWN_SECURITY_'), dir(settings)):
        key = name.replace('WELLKNOWN_SECURITY_', '').lower().capitalize()
        for value in getattr(settings, name):
            lines += [f'{key}: {value}']
        lines += ['']

    return HttpResponse('\n'.join(lines), content_type='text/plain')
