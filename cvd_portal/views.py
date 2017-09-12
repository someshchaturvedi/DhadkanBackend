from cvd_portal.models import Doctor, Patient, PatientData, Device
from cvd_portal.serializers import DoctorSerializer, PatientSerializer,\
    PatientDataSerializer, UserSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse

from rest_framework.exceptions import ParseError
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .fcm import send_message


class PatientDataCreate(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PatientDataSerializer


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


class DoctorList(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

    def get(self, request):
        if request.GET.get('mobile', '') == '':
            return super(DoctorList, self).get(self, request)
        else:
            try:
                d = Doctor.objects.get(
                    mobile=int(request.GET.get('mobile', '')))
            except:
                return JsonResponse(
                    {"Error": "invalid"},
                    safe=False, content_type='application/json')

            return JsonResponse(
                DoctorSerializer(d).data,
                safe=False, content_type='application/json')


class UserDestroy(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(APIView):
    def post(self, request, format=None):

        try:
            data = request.data
            print(data)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        if "user" not in data or "password" not in data:
            return Response(
                'Wrong credentials',
                status=status.HTTP_401_UNAUTHORIZED
            )

        username = data['user']
        password = data['password']

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
               'Username password are not correct',
               status=status.HTTP_404_NOT_FOUND
            )
        response = {}
        response["U_ID"] = user.id

        if Patient.objects.filter(user=user).exists():
            p = Patient.objects.get(user=user)
            response['Type'] = 'patient'
            response['ID'] = p.id
        if Doctor.objects.filter(user=user).exists():
            d = Doctor.objects.get(user=user)
            response['Type'] = 'doctor'
            response['ID'] = d.pk
        else:
            return Response(
                    'Registration not completed',
                    status=status.HTTP_401_UNAUTHORIZED
                )

        Token.objects.filter(user=user).delete()
        token = Token.objects.get_or_create(user=user)
        response['Token'] = token[0].key
        return JsonResponse(
            response, safe=False, content_type='application/json')


class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            Token.objects.filter(user=request.user).delete()
        except ParseError:
            return Response({'status': 'error'})
        return Response({'status': 'done'})


class PatientOnboarding(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        response = {}
        u = User(username=data['mobile'], password=data['password'])
        u.save()
        response['U_ID'] = u.id

        d = Doctor.objects.get(id=data['doctor'])

        p = Patient(
            name=data['name'],
            mobile=data['mobile'],
            email=data['email'],
            address=data['address'],
            # fcm=data['fcm'],
            user=u,
            doctor=d
            )
        p.save()
        response['ID'] = p.id
        t = Token(user=u)
        t.save()
        response['Token'] = t.key

        return JsonResponse(
            response, safe=False, content_type='application/json')


class DocOnboarding(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        response = {}
        u = User(username=data['mobile'], password=data['password'])
        u.save()
        response['U_ID'] = u.id

        d = Doctor(
            name=data['name'],
            mobile=data['mobile'],
            email=data['email'],
            hospital=data['hospital'],
            # fcm=data['fcm'],
            user=u)
        d.save()
        response['ID'] = d.id

        t = Token(user=u)
        t.save()
        response['Token'] = t.key

        return JsonResponse(
            response, safe=False, content_type='application/json')


class DeviceCRUD(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            print(data)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        response = {}

        if data['type'] == 'doctor':
            d = Doctor.objects.get(pk=int(data['id']))
            try:
                if d.device is not None and d.device.device_id == data['fcm']:
                    _id = d.device.id
                else:
                    dev = Device(device_id=data['fcm'])
                    dev.save()
                    d.device = dev
                    d.save()
                    _id = dev.id

            except:
                pass

        elif data['type'] == 'patient':
            p = Patient.objects.get(pk=int(data['id']))
            print(p)
            try:
                if p.device is not None and data['fcm'] == p.device.id:
                    _id = p.device.id
                else:
                    dev = Device(device_id=data['fcm'])
                    dev.save()
                    p.device = dev
                    p.save()
                    _id = dev.id

            except:
                pass
        else:
            return Response(
                'Server Error',
                status=status.HTTP_401_UNAUTHORIZED
            )

        response['pk'] = _id
        return JsonResponse(
            response, safe=False, content_type='application/json')


class NotificationCRUD(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            print(data)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        response = {}
        msg = data['message']
        _to = data['to']
        _from = data['from']
        response['response'] = send_message(_to, _from, msg)
        return JsonResponse(
            response, safe=False, content_type='application/json')
