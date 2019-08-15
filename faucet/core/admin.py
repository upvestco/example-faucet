from django.contrib import admin

from .models import Faucet, DonationRequest

admin.site.register(Faucet)
admin.site.register(DonationRequest)
