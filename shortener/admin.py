from django.contrib import admin
from .models import Urls

# Register your models here.
class UrlsAdmin(admin.ModelAdmin):
    list_display = ["id", "suffix", "url"]
    search_fields = ["suffix", "url"]


admin.site.register(Urls, UrlsAdmin)
