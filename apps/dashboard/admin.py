from django.contrib import admin

from .models import DNSReq, HTTPReq


# Register your models here.
@admin.register(DNSReq)
class AuthorizationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DNSReq._meta.fields if field.name != "id"]


@admin.register(HTTPReq)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HTTPReq._meta.fields if field.name != "id"]
