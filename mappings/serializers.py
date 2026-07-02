from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    assigned_by_email = serializers.StringRelatedField(source='assigned_by', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'patient_details', 'doctor_details', 'assigned_by', 'assigned_by_email', 'notes', 'assigned_at']
        read_only_fields = ['id', 'assigned_by', 'assigned_at']

    def validate(self, data):
        try:
            PatientDoctorMapping.objects.get(patient=data['patient'], doctor=data['doctor'])
            raise serializers.ValidationError('This doctor is already assigned to this patient.')
        except PatientDoctorMapping.DoesNotExist:
            pass
        return data
