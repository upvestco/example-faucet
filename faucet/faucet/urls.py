from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from core.views import FaucetView

urlpatterns = [
    re_path(r'^$', FaucetView.as_view(), name='faucet')
]

if settings.DEBUG:
    urlpatterns += [
    path('admin/', admin.site.urls),
]
