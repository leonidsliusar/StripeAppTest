from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Item(models.Model):
    name = models.CharField()
    description = models.CharField()
    price = models.IntegerField(validators=[MinValueValidator(0)])


class Discount(models.Model):
    redeem_help = ("The max_redemptions and redeem_by values apply to the coupon across every application. "
                   "For example, you can restrict a coupon to the first 50 usages of it, or you can make a "
                   "coupon expire by a certain date.")

    applies = ("You can limit the products that are eligible for discounts using a coupon by adding the product IDs to"
               "the applies_to hash in the Coupon object. Any promotion codes that map to this coupon only apply to "
               "the list of eligible products.")

    class Currency(models.TextChoices):
        DOLLAR = 'USD'
        EURO = 'EUR'
        RUB = 'RUB'

    currency = models.CharField(choices=Currency.choices, default='USD')
    percent_off = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100)])
    max_redemptions = models.IntegerField(blank=True, null=True, help_text=redeem_help)
    redeem_by = models.DateTimeField(blank=True, null=True, help_text=redeem_help)
    applies_to = models.IntegerField(blank=True, null=True, help_text=applies)


class Tax(models.Model):
    display_name = models.CharField()
    inclusive = models.BooleanField(default=False)
    percentage = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100)])
    active = models.BooleanField(blank=True, null=True)
    country = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discounts = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    taxes = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)
