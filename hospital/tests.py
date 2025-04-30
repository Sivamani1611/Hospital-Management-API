from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Patient, MedicalRecord

User = get_user_model()

class PatientTestCase(APITestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(username='doc1', password='test1234', role='doctor')
        self.client.login(username='doc1', password='test1234')

    def test_create_patient(self):
        data = {'name': 'John', 'age': 30, 'gender': 'Male', 'address': 'NY'}
        self.client.force_authenticate(user=self.doctor)
        response = self.client.post('/api/patients/', data)
        self.assertEqual(response.status_code, 201)

    def test_patient_access_control(self):
        other_doctor = User.objects.create_user(username='doc2', password='test1234', role='doctor')
        patient = Patient.objects.create(name='Test', age=40, gender='Male', address='Delhi', created_by=other_doctor)
        self.client.force_authenticate(user=self.doctor)
        response = self.client.get('/api/patients/')
        self.assertNotIn(patient.id, [p['id'] for p in response.data])
