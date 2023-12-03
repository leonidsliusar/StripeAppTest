import datetime
import uuid
from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MaxLengthValidator,
    MinLengthValidator,
)

two_symbol = [MinLengthValidator(2), MaxLengthValidator(2)]
from_0_to_100 = [MinValueValidator(0.0), MaxValueValidator(100)]
not_more_than_5y = [
    MinValueValidator(
        limit_value=datetime.datetime.now() + datetime.timedelta(days=5 * 365)
    )
]
jurisdiction_help = (
    "The jurisdiction for the tax rate. You can use this label field for tax reporting purposes. "
    "It also appears on your customer’s invoice."
)
country_help = "Two-letter country code (ISO 3166-1 alpha-2)"
state_help = "ISO 3166-2 subdivision code, without country prefix. For example, “NY” for New York, United States."
metadata_help = (
    "Set of key-value pairs that you can attach to an object. "
    "This can be useful for storing additional information about the object in a structured format."
)
redeem_help = (
    "The max_redemptions and redeem_by values apply to the coupon across every application. "
    "For example, you can restrict a coupon to the first 50 usages of it, or you can make a "
    "coupon expire by a certain date."
)


class Item(models.Model):
    name = models.CharField()
    description = models.CharField()
    price = models.IntegerField(validators=[MinValueValidator(0)])


class Discount(models.Model):
    class Currency(models.TextChoices):
        DOLLAR = "usd"
        EURO = "eur"
        RUB = "rub"

    class Duration(models.TextChoices):
        once = "once"
        repeat = "repeating"
        forever = "forever"

    currency = models.CharField(choices=Currency.choices, default="usd")
    duration = models.CharField(choices=Duration.choices, default="once", blank=True, null=True)
    percent_off = models.FloatField(validators=from_0_to_100)
    duration_in_months = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    max_redemptions = models.IntegerField(blank=True, null=True, help_text=redeem_help)
    redeem_by = models.DateTimeField(blank=True, null=True, help_text=redeem_help, validators=not_more_than_5y)
    metadata = models.JSONField(blank=True, null=True, help_text=metadata_help)


class Tax(models.Model):
    id = models.CharField(primary_key=True, auto_created=False, default=uuid.uuid4)
    display_name = models.CharField()
    inclusive = models.BooleanField(default=False)
    percentage = models.DecimalField(max_digits=10 * 10, decimal_places=3, validators=from_0_to_100)
    active = models.BooleanField(default=True)
    jurisdiction = models.CharField(blank=True, null=True, help_text=jurisdiction_help)
    country = models.CharField(blank=True, null=True, help_text=country_help, validators=two_symbol)
    description = models.CharField(blank=True, null=True)
    state = models.CharField(blank=True, null=True, help_text=state_help, validators=two_symbol)
    metadata = models.JSONField(blank=True, null=True, help_text=metadata_help)


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(
        Discount, null=True, blank=True, on_delete=models.SET_NULL
    )
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)
