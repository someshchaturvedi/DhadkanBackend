from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    hospital = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    mobile = models.IntegerField(blank=True)
    speciality = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.IntegerField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class PatientData(models.Model):
    patient = models.ForeignKey(Patient, related_name='data')
    bp = models.IntegerField()
    weight = models.IntegerField()
    heart_rate = models.IntegerField()
    time_stamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.patient.first_name + ' ' + self.patient.last_name + ' ' + \
            self.time_stamp
