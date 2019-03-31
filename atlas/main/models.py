from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Chapter(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

    def __str__(self):
        return self.title

class Subheading(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True)
    division = models.CharField(max_length=30, blank=True)
    bookmark = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.user.username

class Exam(models.Model):
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Exam"
        verbose_name_plural = "Exams"

    def __str__(self):
        return self.name

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = RichTextUploadingField(blank=False)
    amount = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=False)
    is_valid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.text

class Examlog(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    participant = models.CharField(max_length=200, blank=True)
    achieved = models.PositiveSmallIntegerField(default=1)
    attempt = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Examlog"
        verbose_name_plural = "Examlogs"

    def __str__(self):
        return self.participant