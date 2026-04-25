from django.contrib import admin
from .models import Address, PaymentMethod

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street_address', 'city', 'state', 'is_default']
    list_filter = ['is_default', 'city', 'state']
    search_fields = ['user__username', 'street_address', 'city']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_type', 'last4', 'is_default']
    list_filter = ['card_type', 'is_default']
    search_fields = ['user__username', 'last4']
