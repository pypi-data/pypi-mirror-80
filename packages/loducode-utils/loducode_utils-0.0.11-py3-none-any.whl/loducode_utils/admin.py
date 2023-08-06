from django.contrib import admin

from loducode_utils.models import City, PaymentRecord


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_at', 'modified_at', 'created_by', 'modified_by'
    )

class ReadOnlyStackedInline(admin.StackedInline):
    readonly_fields = (
        'created_at', 'modified_at', 'created_by', 'modified_by'
    )

class ReadOnlyTabularInline(admin.TabularInline):
    readonly_fields = (
        'created_at', 'modified_at', 'created_by', 'modified_by'
    )

class CityAdmin(ReadOnlyAdmin):
    list_display = ("name","state")
    list_display_links = ("name","state")
    list_filter = ("state",)
    search_fields = ("name",)

admin.site.register(City, CityAdmin)