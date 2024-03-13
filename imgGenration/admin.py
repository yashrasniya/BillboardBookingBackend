from django.contrib import admin
from .models import openAiConfig,generationsHistory

# Register your models here.
@admin.register(openAiConfig)
class openAiConfig(admin.ModelAdmin):
    pass

admin.site.register(generationsHistory)
