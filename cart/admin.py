from django.contrib import admin
from .models import Coupon

# Register your models here.


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount', 'active']
    list_filter = ['code', 'amount', 'active']
    search_fields = ['code']


admin.site.register(Coupon, CouponAdmin)
