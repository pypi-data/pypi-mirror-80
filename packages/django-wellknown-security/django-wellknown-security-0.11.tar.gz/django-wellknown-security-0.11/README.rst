=======================
Well-Known security.txt
=======================

https://securitytxt.org/
A proposed standard which allows websites to define security policies.

based on:
https://adamj.eu/tech/2020/06/28/how-to-add-a-well-known-url-to-your-django-site/

Quick start
-----------
1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'wellknown_security',
    ]

2. Include the polls URLconf in your project urls.py like this::

    from django.conf.urls import include
    ...
    path('.well-known/', include('wellknown_security.urls')),


3. Add at least the contact info to settings.py

   WELLKNOWN_SECURITY_CONTACT = "contact@tld"

4. Start the development server and visit http://127.0.0.1:8000/.well-known/security.txt
   to check the results
