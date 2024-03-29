# Generated by Django 4.2.7 on 2024-01-18 17:07

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(upload_to='author_images/')),
                ('designation', models.CharField(max_length=150)),
                ('phone_number', models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+880 1XXX NNNNNN'. Up to 15 digits allowed.", regex='^\\?1?\\d{9,15}$')])),
                ('email', models.EmailField(max_length=50)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+088'. Up to 15 digits allowed.", regex='^\\?1?\\d{9,15}$')])),
                ('email', models.EmailField(max_length=50)),
                ('message', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=350, null=True)),
                ('duration', models.PositiveIntegerField(default=0)),
                ('skill_level', models.CharField(choices=[('Advanced', 'Advanced'), ('Intermediate', 'Intermediate'), ('Basic', 'Basic')], default='Basic', max_length=50)),
                ('language', models.CharField(choices=[('Bangla', 'Bangla'), ('English', 'English')], default='Bangla', max_length=20)),
                ('course_details', ckeditor.fields.RichTextField()),
                ('banner', models.ImageField(upload_to='courses_banner/')),
                ('price', models.PositiveIntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_author', to='lms.author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_category', to='lms.category')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='Teams_members/')),
                ('designation', models.CharField(max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+880 1XXX NNNNNN'. Up to 15 digits allowed.", regex='^\\?1?\\d{9,15}$')])),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('fb', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courses', models.ManyToManyField(to='lms.course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('is_preview', models.BooleanField(default=False)),
                ('video_file', models.FileField(upload_to='course_videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])])),
                ('class_file', models.FileField(blank=True, null=True, upload_to='course_files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'docx'])])),
                ('assignment', models.FileField(blank=True, null=True, upload_to='assignment_files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'jpg'])])),
                ('quiz', models.URLField(blank=True, max_length=500, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='lms.course')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=20)),
                ('transaction_id', models.CharField(max_length=50, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+880 1XXX NNNNNN'. Up to 15 digits allowed.", regex='^\\?1?\\d{9,15}$')])),
                ('name', models.CharField(max_length=100)),
                ('department', models.CharField(choices=[('CSE', 'Computer Science and Engineering'), ('EEE', 'Electrical and Electronics Engineering'), ('CE', 'Civil Engineering'), ('ENGLISH', 'English'), ('BBA', 'Bachelor of Business Administration'), ('MECHANICAL', 'Mechanical Engineering')], max_length=50)),
                ('semester', models.CharField(choices=[('1', 'Semester 1'), ('2', 'Semester 2'), ('3', 'Semester 3'), ('4', 'Semester 4'), ('5', 'Semester 5'), ('6', 'Semester 6'), ('7', 'Semester 7'), ('8', 'Semester 8')], max_length=20)),
                ('approved', models.BooleanField(default=False)),
                ('batch_no', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('course_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
