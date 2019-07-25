from django.conf import settings
from upvest.clientele import UpvestClienteleAPI


def get_wallet():
    api = UpvestClienteleAPI(
        settings.UPVEST_OAUTH_CLIENT_ID,
        settings.UPVEST_OAUTH_CLIENT_SECRET,
        settings.UPVEST_USERNAME,
        settings.UPVEST_PASSWORD,
        base_url=settings.UPVEST_BACKEND,
    )
    return api.wallets.get(settings.UPVEST_WALLET_ID)
