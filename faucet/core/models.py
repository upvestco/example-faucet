from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from .utils import get_wallet


def send_eth(address, ip):
    DonationRequest.objects.create(address=address, ip=ip)

    wallet = get_wallet()

    quantity = int(0.01 * (10 ** 18))
    fee = int(0.0001 * (10 ** 18))
    return wallet.transactions.create(settings.UPVEST_PASSWORD, settings.ASSET_ID, quantity, fee, address)


def greylisted(address, ip):
    if ip == "213.61.201.242":
        # perma-whitelist upvest office IP
        return None
    qs = DonationRequest.objects.filter(address=address) | DonationRequest.objects.filter(ip=ip)
    cooldown = timedelta(seconds=settings.GREYLIST_COOLDOWN)
    cooldown_at = timezone.now() - cooldown
    latest_request = qs.filter(requested__gte=cooldown_at).order_by("-requested").first()
    return None if latest_request is None else (latest_request.requested + cooldown)


class DonationRequest(models.Model):

    address = models.CharField(max_length=42)
    """ The wallet to send ETH to """

    ip = models.GenericIPAddressField()
    """ The IP address making the request """

    requested = models.DateTimeField(auto_now_add=True)
    """ When this was requested - for greylisting purposes """

    def __str__(self):
        return "%s requested by %s at %s" % (self.address, self.ip, self.requested)
