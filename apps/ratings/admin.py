from django.contrib import admin
from .models import Rating


class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'value',)

    # search_fields = ('full_name',)

    # @admin.display()
    # def full_name(self, obj):
    #     return obj.user.get_full_name()


admin.site.register(Rating, RatingAdmin)
