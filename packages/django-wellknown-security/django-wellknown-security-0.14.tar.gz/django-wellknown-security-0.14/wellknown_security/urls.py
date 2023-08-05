# -*- coding: utf-8 -*-
__author__ = "Peter Gastinger"
__copyright__ = "Copyright 2020"
__credits__ = ["Peter Gastinger"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Peter Gastinger"
__email__ = "peter@secitec.net"
__status__ = "Production"

from django.urls import path
from .views import security_txt

urlpatterns = [
    path("security.txt", security_txt),
]
