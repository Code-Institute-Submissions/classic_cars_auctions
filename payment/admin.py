from django.contrib import admin
from .models import Payment, PaymentLineItem


class PaymentLineItemAdminInline(admin.TabularInline):
    """PaymentLineItemAdminInline"""
    model = PaymentLineItem
    readonly_fields = ('car_price',)


class PaymentAdmin(admin.ModelAdmin):
    """PymentAdmin"""
    inlines = (PaymentLineItemAdminInline,)

    readonly_fields = ('payment_number', 'date',
                       'deposit',)

    fields = ('payment_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'deposit',)

    list_display = ('payment_number', 'date', 'full_name',
                    'deposit',)

    ordering = ('-date',)


admin.site.register(Payment, PaymentAdmin)
