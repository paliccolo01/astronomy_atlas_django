from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Subheading(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    division = models.CharField(max_length=30, blank=True)
    bookmark = models.PositiveSmallIntegerField(blank=True)

    def __str__(self):
        return self.user.username
