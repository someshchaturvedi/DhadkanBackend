from django.contrib import admin
from cvd_portal.models import Doctor, Patient, PatientData, Device, Image

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(PatientData)
admin.site.register(Device)
admin.site.register(Image)
