from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('patients/', PatientListCreateView.as_view(), name='patients'),
    path('patients/records/add', AddMedicalRecordView.as_view(), name='add-record'),
    path('patients/<int:id>/records/', PatientMedicalRecordsView.as_view(), name='view-records'),
]
