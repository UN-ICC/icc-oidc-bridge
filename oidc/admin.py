from django.contrib import admin
from oidc.models import MappedUrl, AuthSession, PresentationConfigurations

# Register your models here.


@admin.register(MappedUrl)
class MappedUrlAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "modified")


@admin.register(AuthSession)
class AuthSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "presentation_record_id",
        "presentation_request_satisfied",
        "created",
        "modified",
    )


@admin.register(PresentationConfigurations)
class PresentatioCOnfigurationAdmin(admin.ModelAdmin):
    list_display = ("id", "subject_identifier")
