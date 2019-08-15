# Generated by Django 2.2.3 on 2019-08-15 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DonationRequest",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("address", models.CharField(max_length=42)),
                ("ip", models.GenericIPAddressField()),
                ("requested", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Faucet",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("asset_code", models.CharField(max_length=12)),
                ("name", models.CharField(max_length=120)),
                ("asset_id", models.UUIDField(unique=True)),
                ("wallet_id", models.UUIDField()),
                ("wallet_address", models.CharField(max_length=64)),
                ("sending_amount", models.DecimalField(decimal_places=5, max_digits=20)),
                ("visible", models.BooleanField()),
            ],
        ),
    ]
