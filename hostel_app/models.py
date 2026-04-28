from django.db import models
from django.contrib.auth.models import User


# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    room_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


# Room Model
class Room(models.Model):
    room_number = models.IntegerField()
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)

    def __str__(self):
        return str(self.room_number)


# Fee Model
class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=10, default="Pending")
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.amount)


# Complaint Model
class Complaint(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="General")  # ← ADDED
    message = models.TextField()
    status = models.CharField(max_length=50, default="Pending")
    priority = models.CharField(max_length=20, default="Medium")
    category = models.CharField(max_length=20, default="General")

    def __str__(self):
        return self.title


# Notice Model
class Notice(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Warden Model
class Warden(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


# Visitor Model
class Visitor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=200, default="Visit")
    entry_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.visitor_name


# Activity Model
class Activity(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message