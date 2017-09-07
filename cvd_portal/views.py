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
from rest_framework import status


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


class DoctorList(generics.ListCreateAPIView):
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


class UserCreate(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        u = User(username=username)
        u.set_password(password)
        u.save()
        return JsonResponse(
            {"id": u.id}, safe=False, content_type='application/json')


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
            user=u)
        d.save()
        response['ID'] = d.id

        t = Token(user=u)
        t.save()
        response['Token'] = t.key

        return JsonResponse(
            response, safe=False, content_type='application/json')
