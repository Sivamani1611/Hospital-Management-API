from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Patient, MedicalRecord
from .serializers import *
from .permissions import IsDoctorOwner
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes

class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid Credentials'}, status=400)

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Patient.objects.all()
        return Patient.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AddMedicalRecordView(APIView):
    def post(self, request):
        patient_id = request.data.get('patient')
        try:
            patient = Patient.objects.get(id=patient_id)
            if patient.created_by != request.user and not request.user.is_superuser:
                return Response({'error': 'Not allowed'}, status=403)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)

        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class PatientMedicalRecordsView(generics.ListAPIView):
    serializer_class = MedicalRecordSerializer

    def get_queryset(self):
        patient_id = self.kwargs['id']
        patient = Patient.objects.get(id=patient_id)
        if patient.created_by != self.request.user and not self.request.user.is_superuser:
            return MedicalRecord.objects.none()
        return MedicalRecord.objects.filter(patient=patient)
