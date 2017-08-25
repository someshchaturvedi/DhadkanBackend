from django.conf.urls import url
from rest_framework.authtoken import views
from cvd_portal.views import PatientDetail, PatientList, UserCreate, \
    UserDestroy, PatientDataDetail, DoctorDetail, DoctorList, Logout
urlpatterns = [
    url(r'api/patient/(?P<pk>[0-9]+)$', PatientDetail.as_view()),
    url(r'api/patient$', PatientList.as_view()),
    url(r'api/doctor/(?P<pk>[0-9]+)$', DoctorDetail.as_view()),
    url(r'api/doctor$', DoctorList.as_view()),
    url(r'api/user$', UserCreate.as_view()),
    url(r'api/user/(?P<pk>[0-9]+)$', UserDestroy.as_view()),
    url(r'api/data/(?P<pk>[0-9]+)$', PatientDataDetail.as_view()),
    url(r'api/login$', views.obtain_auth_token),
    url(r'api/logout$', Logout.as_view()),
]
