from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.utils import timezone
#for enroll
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

#for ss
from django.contrib.auth.models import AbstractUser


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='author_images/')
    designation = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Course(models.Model):
    ADVANCED = 'Advanced'
    INTERMEDIATE = 'Intermediate'
    BASIC = 'Basic'
    SKILL_CHOICES = [
        (ADVANCED,'Advanced'),
        (INTERMEDIATE,'Intermediate'),
        ( BASIC ,'Basic'),  
    ]

    BANGLA = 'Bangla'
    ENGLISH = 'English'
    LANGUAGE_CHOOSE = [
        (BANGLA ,'Bangla'),
        (ENGLISH ,'English'),
    ]


    author = models.ForeignKey(Author, related_name='course_author', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='course_category', on_delete=models.CASCADE)
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField( max_length=350, null=True, blank=True)
    duration = models.PositiveIntegerField(default=0)
    skill_level = models.CharField(max_length=50, choices=SKILL_CHOICES, default=BASIC)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOOSE, default=BANGLA)
    course_details = RichTextField()
    banner = models.ImageField(upload_to='courses_banner/')
    course_files = models.FileField(upload_to='course_files/',null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Video(models.Model):
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    is_preview = models.BooleanField(default=False)
    video_file = models.FileField(upload_to='course_videos/')
    class_file = models.FileField(upload_to='course_files/')

    def __str__(self):
        return self.title


# for enroll ment 

  # models.py

class Enrollment(models.Model):
    SEMESTER_CHOICES = [
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
        ('3', 'Semester 3'),
        ('4', 'Semester 4'),
        ('5', 'Semester 5'),
        ('6', 'Semester 6'),
        ('7', 'Semester 7'),
        ('8', 'Semester 8'),
    ]

    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('CE', 'Civil Engineering'),
        ('ENGLISH', 'English'),
        ('BBA', 'Bachelor of Business Administration'),
        ('MECHANICAL', 'Mechanical Engineering'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=50, unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  # Example regex for international phone numbers
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)

    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    # Add the course_price field to store the price for this enrollment
    course_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.student_id


