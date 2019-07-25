import re
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timesince import timeuntil
from django.views import View

from .models import greylisted, send_eth
from .utils import get_wallet

WALLET_RE = re.compile(r"^0x[a-fA-F0-9]{30,40}$")


def _get_balance():
    wallet = get_wallet()
    for bal in wallet.balances:
        if bal["asset_id"] == settings.ASSET_ID:
            return Decimal(bal["amount"]) / (10 ** bal["exponent"])
    return "NOT FOUND"


def _get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class FaucetView(View):

    curl = False

    def get(self, request, *args, **kwargs):
        if self.curl:
            ip = _get_client_ip(request)
            address = kwargs["address"]
            cooldown_at = greylisted(address, ip)
            if cooldown_at:
                return JsonResponse(
                    {"message": "You are greylisted for another %s" % timeuntil(cooldown_at)}, status=403
                )
            else:
                tx = send_eth(address, ip)
                return JsonResponse(
                    {"message": "Request received successfully. 0.01ETH will be sent to %s" % address, "tx": tx.txhash},
                    status=200,
                )
        return render(request, "faucet.html", context={"balance": _get_balance()})

    def post(self, request, *args, **kwargs):
        address = request.POST.get("address")
        ctx = {"address": address, "balance": _get_balance()}
        if not address:
            messages.error(request, "You must supply a wallet address")
        elif not WALLET_RE.match(address):
            messages.error(request, "That does not seem to be a valid wallet address")
        else:
            ip = _get_client_ip(request)
            cooldown_at = greylisted(address, ip)
            if cooldown_at:
                messages.warning(request, "You are greylisted for another %s" % timeuntil(cooldown_at))
            else:
                tx = send_eth(address, ip)
                messages.info(request, "Request received successfully. 0.01ETH will be sent to %s" % address)
                ctx["tx"] = tx

        return render(request, "faucet.html", context=ctx)
