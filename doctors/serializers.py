from rest_framework import serializers
from .models import Doctor
import re


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'email', 'phone', 'specialization', 'license_number', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        doctor = Doctor.objects.filter(email=value)
        if self.instance:
            doctor = doctor.exclude(id=self.instance.id)
        if doctor.exists():
            raise serializers.ValidationError('Doctor with this email already exists.')
        return value

    def validate_phone(self, value):
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError('Invalid phone number format.')
        return value

    def validate_license_number(self, value):
        doctor = Doctor.objects.filter(license_number=value)
        if self.instance:
            doctor = doctor.exclude(id=self.instance.id)
        if doctor.exists():
            raise serializers.ValidationError('License number already registered.')
        if not re.match(r'^[A-Z]{2,}\d{4,}$', value):
            raise serializers.ValidationError('Invalid license format. Use format like MD123456.')
        return value
