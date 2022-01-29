from django.contrib import admin
from apps.chats import models as chat_models


@admin.register(chat_models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("content",)
