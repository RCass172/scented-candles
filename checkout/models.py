""" Imports """
import uuid
from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django_countries.fields import CountryField
from products.models import Product
from profiles.models import UserProfile
from cart.models import Coupon


# Taken from Code institute Boutique Ado project
class Order(models.Model):
    """ Allows creation and tracking of orders """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """ Generates a unique order number using UUID """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Update grand total for line item added inc. delivery costs"""
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        # Check if coupon
        if self.coupon is not None:
            discount = self.lineitems.aggregate(
                Sum('lineitem_total'))['lineitem_total__sum']*(self.coupon.amount/Decimal('100'))
            self.delivery_cost = 5
            self.grand_total = self.order_total + self.delivery_cost - discount
            self.save()
        else:
            self.delivery_cost = 5
            self.grand_total = self.order_total + self.delivery_cost
            self.save()

    def save(self, *args, **kwargs):
        """Override the original save method to set the order number"""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        """ Returns the order number """
        return self.order_number


class OrderLineItem(models.Model):
    """ Defines an individual product in order """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        """ Returns SKU and order number for each product """
        return f'SKU {self.product.sku} on order {self.order.order_number}'
