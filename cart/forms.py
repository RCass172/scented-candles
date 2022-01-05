from django import forms
from .models import Coupon


class CouponApplyForm(forms.Form):
    code = forms.CharField()

    class Meta:
        model = Coupon
        fields = (
            'code',
        )
