# Generated by Django 3.2.9 on 2022-01-04 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0007_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='content',
        ),
    ]