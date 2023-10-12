
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# Create your models here.

class TeacherUserManager(BaseUserManager):
    def create_user(self, username, email, teacher_id, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, teacher_id=teacher_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, teacher_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, teacher_id, password, **extra_fields)


class TeacherUser(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=10, )
    lastname = models.CharField(max_length=10, )
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    teacher_id = models.CharField(max_length=10, unique=True)
    # Add other fields here
    is_superuser = models.BooleanField(default=False)  
    is_teacher = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = TeacherUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'teacher_id']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.username

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Class(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    teacher = models.ForeignKey('TeacherUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    ID = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student} - {self.date} ({self.is_present})'
