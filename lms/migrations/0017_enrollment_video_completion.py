# Generated by Django 4.2.7 on 2024-01-16 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0016_author_email_author_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='video_completion',
            field=models.JSONField(default=dict),
        ),
    ]