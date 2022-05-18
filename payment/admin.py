from django.contrib import admin
from .models import Payment


# class PaymentLineItemAdminInline(admin.TabularInline):
#     """PaymentLineItemAdminInline"""
#     model = PaymentLineItem
#     readonly_fields = ('car_price',)


class PaymentAdmin(admin.ModelAdmin):
    """PymentAdmin"""
    # inlines = (PaymentLineItemAdminInline,)

    readonly_fields = ('payment_number', 'date',
                       'deposit', 'car', 'bids')

    fields = ('payment_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'deposit', 'car', 'bids')

    list_display = ('payment_number', 'date', 'full_name',
                    'deposit', 'car', 'bids')

    ordering = ('-date',)


admin.site.register(Payment, PaymentAdmin)
