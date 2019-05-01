from django.db import models


# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=12, default="000.000.0000")
    name = models.CharField(max_length=50, default="DEFAULT")
    type = models.CharField(max_length=20, default="person")
    isLoggedOn = models.BooleanField(default=False)


class Course(models.Model):
    course_id = models.CharField(max_length=10)
    num_labs = models.IntegerField(default=0)
    instructor = models.CharField(max_length=50, default="no Instructor")
    # temp disabled
    # tee_ays = models.ForeignKey(ModelTA, on_delete=models.CASCADE)


class Lab(models.Model):
    TA = models.CharField(max_length=50, default="no TA")
    section_id = models.IntegerField(default=0)
    course_id = models.CharField(max_length=10)


class TACourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    TA = models.ForeignKey(User, on_delete=models.CASCADE)
