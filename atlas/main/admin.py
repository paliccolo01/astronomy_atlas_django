from django.contrib import admin
from .models import Chapter, Subheading, Profile

class ContentAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Fejezet:", {"fields": ["chapter"]}),
        ("Cim:", {"fields": ["title"]}),
        ("Tartalom:", {"fields": ["content"]}),
        ("URL", {"fields": ["slug"]})
    ]

# Register your models here.
admin.site.register(Chapter)
admin.site.register(Subheading)
admin.site.register(Profile)