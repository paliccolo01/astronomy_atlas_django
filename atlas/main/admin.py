from django.contrib import admin
from .models import Chapter, Subheading, Profile
from .models import Exam, Examlog, Question, Answer

class ContentAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Fejezet:", {"fields": ["chapter"]}),
        ("Cim:", {"fields": ["title"]}),
        ("Tartalom:", {"fields": ["content"]}),
    ]

class AnswerTabularInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerTabularInline]

    class Meta:
        model = Question

# Register your models here.
admin.site.register(Chapter)
admin.site.register(Subheading)
admin.site.register(Profile)

admin.site.register(Exam)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Examlog)