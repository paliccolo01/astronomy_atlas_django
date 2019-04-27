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
        ordering = ["pk"]

    def __str__(self):
        return self.title

class Subheading(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True)

    class Meta:
        verbose_name = "Subheading"
        verbose_name_plural = "Subheadings"
        ordering = ["pk"]

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
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, blank=True)
    goal = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Exam"
        verbose_name_plural = "Exams"
        ordering = ["pk"]

    def __str__(self):
        return self.name

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = RichTextUploadingField(blank=False)
    amount = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["pk"]

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=False)
    is_valid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ["pk"]

    def __str__(self):
        return self.text

class Examlog(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    participant = models.CharField(max_length=200, blank=True)
    achieved = models.PositiveSmallIntegerField(default=1)
    passed = models.BooleanField(default=False)
    attempt = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Examlog"
        verbose_name_plural = "Examlogs"
        ordering = ["pk"]

    def __str__(self):
        return self.participant