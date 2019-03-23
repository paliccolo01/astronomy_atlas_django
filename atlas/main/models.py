from django.db import models

# Create your models here.
class Subheading(models.Model):
    subheading_title = models.CharField(max_length=200)
    subheading_content = models.TextField()

    def __str__(self):
        return self.subheading_title