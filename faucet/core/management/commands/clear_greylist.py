from django.core.management.base import BaseCommand

from core.models import DonationRequest


class Command(BaseCommand):
    help = "Clear the greylist"

    def handle(self, *args, **options):
        print("%d requests deleted" % DonationRequest.objects.all().delete()[0])
