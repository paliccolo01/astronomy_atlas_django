from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Chapter(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, blank=True)
    slug = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

    def __str__(self):
        return self.title


class Subheading(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True)
    slug = models.CharField(max_length=200, default=1)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True)
    division = models.CharField(max_length=30, blank=True)
    bookmark = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.user.username
