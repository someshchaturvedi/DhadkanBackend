from rest_framework import serializers
from cvd_portal.models import Doctor, Patient, PatientData
from django.contrib.auth.models import User


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DoctorSerializer(DynamicFieldsModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Doctor
        fields = [
            'pk',
            'first_name',
            'last_name',
            'hospital',
            'email',
            'mobile',
            'speciality',
            'designation',
            'user'
        ]


class PatientDataSerializer(DynamicFieldsModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all())

    class Meta:
        model = PatientData
        fields = [
            'pk',
            'bp',
            'weight',
            'heart_rate',
            'time_stamp',
            'patient'
        ]


class PatientSerializer(DynamicFieldsModelSerializer):
    data = PatientDataSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Patient
        fields = [
            'pk',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'data',
            'user'
        ]


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'password'
        ]
