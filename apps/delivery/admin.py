from django.contrib import admin

from apps.delivery.models import Courier, Category, Job


class CourierAdmin(admin.ModelAdmin):
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


class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'customer', 'courier', 'category',
                    'size', 'quantity', 'created_at')
    # search_fields = ('category',)
    readonly_fields = ('created_at', 'picked_up_at', 'delivered_at')
    list_filter = ('category', 'status')


admin.site.register(Courier, CourierAdmin)
admin.site.register(Category)
admin.site.register(Job, JobAdmin)
