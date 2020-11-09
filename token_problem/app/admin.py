from django.contrib import admin
from app.models import Token

# Register your models here.


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "token",
        "created_time",
        "expire_time",
        "last_used",
        "is_assigned",
        "deleted",
    )
