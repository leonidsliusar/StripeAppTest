from typing import TypeVar
from stripeapp.paymentAPI.manager import (
    StripeManagerExtend,
    ExtendedDiscount,
    ExtendedTax,
)
from django.db.models.signals import post_delete, post_save, pre_save, pre_init
from django.dispatch import receiver
from ..models import Tax, Discount
from ..paymentAPI.exception import PaymentSystemException

M = TypeVar("M", Tax, Discount)


@receiver(pre_save, sender=Tax)
@receiver(pre_save, sender=Discount)
def dispatch_add(instance: M, *args, **kwargs):
    if instance._state.adding:
        manager = StripeManagerExtend()
        if isinstance(instance, Discount):
            on_add_coupon(instance, manager)
        elif isinstance(instance, Tax):
            on_add_tax(instance, manager)


@receiver(post_save, sender=Tax)
@receiver(post_save, sender=Discount)
def dispatch_save(instance: M, created: bool, *args, **kwargs):
    if not created:
        manager = StripeManagerExtend()
        if isinstance(instance, Discount):
            on_update_coupon(instance, manager)
        elif isinstance(instance, Tax):
            on_update_tax(instance, manager)


@receiver(post_delete, sender=Tax)
@receiver(post_delete, sender=Discount)
def dispatch_delete(instance: M, *args, **kwargs):
    manager = StripeManagerExtend()
    if isinstance(instance, Discount):
        on_discard_coupon(instance, manager)
    elif isinstance(instance, Tax):
        on_discard_tax(instance, manager)


def on_add_coupon(instance: Discount, manager: ExtendedDiscount):
    try:
        coupon_map = manager.new_coupon(instance)
        instance.pk = coupon_map.get("id")
    except PaymentSystemException:
        ...


def on_update_coupon(instance: Discount, manager: ExtendedDiscount):
    try:
        manager.update_coupon(instance)
    except PaymentSystemException:
        ...


def on_discard_coupon(instance: Discount, manager: ExtendedDiscount):
    try:
        manager.delete_coupon(instance.pk)
    except PaymentSystemException:
        ...


def on_add_tax(instance: Tax, manager: ExtendedTax):
    try:
        tax_map = manager.new_tax(instance)
        instance.pk = tax_map.get("id")
    except PaymentSystemException:
        ...


def on_update_tax(instance: Tax, manager: ExtendedTax):
    try:
        manager.update_tax(instance, instance.pk)
    except PaymentSystemException:
        ...


def on_discard_tax(instance: Tax, manager: ExtendedTax):
    try:
        manager.delete_tax(instance.pk)
    except PaymentSystemException:
        ...
