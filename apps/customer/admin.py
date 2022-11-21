from django.contrib import admin

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user_name', 'phone_number', 'date_joined')

    # search_fields = ('full_name',)

    @admin.display()
    def full_name(self, obj):
        return obj.user.get_full_name()

    @admin.display()
    def user_name(self, obj):
        return obj.user.username

    @admin.display()
    def phone_number(self, obj):
        return obj.user.phone_number

    @admin.display()
    def date_joined(self, obj):
        return obj.user.date_joined


admin.site.register(Customer, CustomerAdmin)
