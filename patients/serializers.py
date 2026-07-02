from rest_framework import serializers
from .models import Patient
import re


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'email', 'phone', 'date_of_birth', 'medical_history', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError('Invalid email format.')
        return value

    def validate_phone(self, value):
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError('Invalid phone number format.')
        return value

    def validate_date_of_birth(self, value):
        from datetime import date
        age = (date.today() - value).days // 365
        if age < 0 or age > 150:
            raise serializers.ValidationError('Invalid date of birth.')
        return value
