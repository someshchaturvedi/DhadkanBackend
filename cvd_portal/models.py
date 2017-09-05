from django.db import models
from django.contrib.auth.models import User
import datetime


class Doctor(models.Model):
    name = models.CharField(max_length=60, default="Somesh")
    hospital = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    mobile = models.IntegerField(blank=True)
    speciality = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=60, default="Somesh")
    date_of_birth = models.DateField(default=datetime.date.today)
    gender = models.IntegerField(default=1)
    email = models.EmailField(blank=True)
    address = models.TextField(null=True)
    doctor = models.ForeignKey(Doctor, related_name="patients", null=True)
    mobile = models.IntegerField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class PatientData(models.Model):
    patient = models.ForeignKey(Patient, related_name='data')
    systolic = models.IntegerField()
    diastolic = models.IntegerField(default=0)
    weight = models.IntegerField()
    heart_rate = models.IntegerField()
    time_stamp = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.patient.name + ' ' + str(self.time_stamp)
