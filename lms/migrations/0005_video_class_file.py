# Generated by Django 5.0 on 2023-12-25 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0004_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='class_file',
            field=models.FileField(default=0, upload_to='course_files/'),
            preserve_default=False,
        ),
    ]
