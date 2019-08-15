import re
from django.conf import settings

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timesince import timeuntil
from django.views import View

from .models import greylisted, Faucet

WALLET_RE = re.compile(r"^0x[a-fA-F0-9]{30,40}$")


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
        asset = kwargs.get("asset")
        if asset is not None:
            faucet = get_object_or_404(Faucet, asset_code__iexact=asset)
        else:
            faucet = Faucet.objects.first()

        if self.curl:
            # the "API" version
            ip = _get_client_ip(request)
            address = kwargs["address"]

            for skip_header in settings.WHITELISTED_HEADERS:
                header = "HTTP_%s" % skip_header.replace("-", "_")
                if header in request.META:
                    cooldown_at = None
                    break
            else:
                cooldown_at = greylisted(address, ip)

            if cooldown_at:
                return JsonResponse(
                    {"message": "You are greylisted for another %s" % timeuntil(cooldown_at)}, status=403
                )
            else:
                tx = faucet.send(address, ip)
                amount = "%s%s" % (faucet.sending_amount.normalize(), faucet.asset_code)
                return JsonResponse(
                    {
                        "message": "Request received successfully. %s will be sent to %s" % (amount, address),
                        "tx": tx.txhash,
                    },
                    status=200,
                )

        # also list other faucets to get links to other assets other than the chosen one
        faucets = Faucet.objects.filter(visible=True).order_by("asset_code")

        return render(request, "faucet.html", context={"faucets": faucets, "faucet": faucet})

    def post(self, request, *args, **kwargs):
        address = request.POST.get("address")
        faucet = get_object_or_404(Faucet, asset_code__iexact=request.POST.get("asset"))

        faucets = Faucet.objects.filter(visible=True).order_by("asset_code")
        ctx = {"address": address, "faucets": faucets, "faucet": faucet}
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
                tx = faucet.send(address, ip)

                amount = "%s%s" % (faucet.sending_amount.normalize(), faucet.asset_code)
                messages.info(request, "Request received successfully. %s will be sent to %s" % (amount, address))
                ctx["tx"] = tx

        return render(request, "faucet.html", context=ctx)
