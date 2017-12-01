from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator


# Create your models here.

class User(AbstractUser):
    # Choices
    gender_choices = {

    }

    # Primary Key
    user_id = models.AutoField(primary_key=True)

    # Foreign Keys
    cities = models.ForeignKey('Cities', on_delete=models.CASCADE,null=True, blank=True)

    born_date = models.DateField(auto_now=False, auto_now_add=False, default = timezone.now)
    gender = models.CharField(max_length=5, choices=gender_choices, null=True)
    photo = models.ImageField(upload_to='uploads', height_field=None, width_field=None, max_length=100, null=True, blank=True)
    user_note = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    def __str__(self):  # __unicode__ on Python 2
        return self.username


class UserContact(models.Model):
    # Primary Key
    user_contact_id = models.AutoField(primary_key=True)

    # Foreign Keys
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=15)
    mail = models.EmailField()
    timestamp = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    def __str__(self):  # __unicode__ on Python 2
        return self.mail


class UserEducation(models.Model):
    # Primary Key
    user_education_id = models.AutoField(primary_key=True)

    # Foreign Keys
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    education_type_id = models.ForeignKey('UserEducationTypes', on_delete=models.CASCADE)
    college_id = models.ForeignKey('Colleges', on_delete=models.CASCADE)
    faculty_id = models.ForeignKey('Faculties', on_delete=models.CASCADE)
    department_id = models.ForeignKey('Departments', on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    def __str__(self):  # __unicode__ on Python 2
        return self.education_type_id


class UserEducationTypes(models.Model):
    # Primary Key
    education_type_id = models.AutoField(primary_key=True)

    type_name = models.CharField(max_length=20)

    def __str__(self):  # __unicode__ on Python 2
        return self.type_name


class Colleges(models.Model):
    # Choices
    college_type_choices = {

    }
    # Primary Key
    college_id = models.AutoField(primary_key=True)

    # Foreign Keys
    cities = models.ForeignKey('Cities', on_delete=models.CASCADE)

    college_name = models.CharField(max_length=50)
    college_type = models.CharField(max_length=10, choices=college_type_choices)

    def __str__(self):  # __unicode__ on Python 2
        return self.college_name


class Faculties(models.Model):
    # Primary Key
    faculty_id = models.AutoField(primary_key=True)

    faculty_name = models.CharField(max_length=20)

    def __str__(self):  # __unicode__ on Python 2
        return self.faculty_name


class Departments(models.Model):
    # Primary Key
    department_id = models.AutoField(primary_key=True)

    department_name = models.CharField(max_length=30)

    def __str__(self):  # __unicode__ on Python 2
        return self.department_name


class Cities(models.Model):
    # Primary Key
    city_id = models.AutoField(primary_key=True)

    city_name = models.CharField(max_length=30)

    def __str__(self):  # __unicode__ on Python 2
        return self.city_name


#DATABASE CALLBACKS
User = get_user_model()

def user_pre_save(sender, instance, *args, **kwargs):

    if not instance.slug or instance.slug == '':
        instance.slug = unique_slug_generator(instance)

pre_save.connect(user_pre_save, sender=User)