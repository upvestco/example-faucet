from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from core.views import FaucetView

urlpatterns = [
    re_path(r"^$", csrf_exempt(FaucetView.as_view(curl=False)), name="faucet"),
    re_path(
        r"^send/0x(?P<address>[a-fA-F0-9]{30,40})$", csrf_exempt(FaucetView.as_view(curl=True)), name="faucet_curl"
    ),
]

if settings.DEBUG:
    urlpatterns += [path("admin/", admin.site.urls)]
