from django.contrib import admin
from cvd_portal.models import Doctor, Patient, PatientData, Device

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(PatientData)
admin.site.register(Device)
