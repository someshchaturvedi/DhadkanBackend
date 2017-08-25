from cvd_portal.models import Doctor, Patient, PatientData
from cvd_portal.serializers import DoctorSerializer, PatientSerializer,\
    PatientDataSerializer, UserSerializer

from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.exceptions import ParseError
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class PatientDataDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = PatientData.objects.all()
    serializer_class = PatientDataSerializer


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class UserCreate(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        u = User(username=username)
        u.set_password(password)
        u.save()
        return JsonResponse(u.id, safe=False, content_type='application/json')


class UserDestroy(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            Token.objects.filter(user=request.user).delete()
        except ParseError:
            return Response({'status': 'error'})
        return Response({'status': 'done'})
