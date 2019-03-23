# Generated by Django 2.1.5 on 2019-03-23 19:09

import ckeditor.fields
from django.db import migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subheading',
            old_name='subheading_title',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='subheading',
            name='subheading_content',
        ),
        migrations.AddField(
            model_name='subheading',
            name='content',
            field=ckeditor.fields.RichTextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
