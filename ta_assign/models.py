from django.db import models
import datetime


# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=12, default="000.000.0000")
    name = models.CharField(max_length=50, default="DEFAULT")
    type = models.CharField(max_length=20, default="person")
    isLoggedOn = models.BooleanField(default=False)
    address = models.CharField(max_length=100, default="not set")


class Course(models.Model):
    course_department = models.CharField(max_length=8)
    course_id = models.PositiveSmallIntegerField(default=0)
    course_dept_id = models.CharField(max_length=9)
    num_lectures = models.PositiveSmallIntegerField(default=0)
    num_labs = models.PositiveSmallIntegerField(default=0)
    current_num_TA = models.PositiveSmallIntegerField(default=0)
    current_num_lectures = models.PositiveSmallIntegerField(default=0)
    current_num_labs = models.PositiveSmallIntegerField(default=0)


class Lecture(models.Model):
    instructor = models.CharField(max_length=50, default="no instructor")
    TA = models.CharField(max_length=50, default="no TA")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecture_section = models.CharField(max_length=3)
    lecture_location = models.CharField(max_length=50, default="NOT SET")
    lecture_time = models.TimeField(default=datetime.time(00, 00))


class Lab(models.Model):
    TA = models.CharField(max_length=50, default="no TA")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lab_section = models.CharField(max_length=3)
    lab_location = models.CharField(max_length=50, default="NOT SET")
    lab_time = models.TimeField(default=datetime.time(00, 00))


class InstructorCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)


class TACourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    TA = models.ForeignKey(User, on_delete=models.CASCADE)
