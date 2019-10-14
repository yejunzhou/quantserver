from django.contrib import admin

# Register your models here.
from remind.models import Custom


class CustomAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Custom._meta.fields]


admin.site.register(Custom, CustomAdmin)
