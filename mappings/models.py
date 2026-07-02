from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from authentication.models import User


class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctors', db_index=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='patients', db_index=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='doctor_assignments')
    notes = models.TextField(blank=True, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'patient_doctor_mappings'
        unique_together = ['patient', 'doctor']
        indexes = [
            models.Index(fields=['patient', 'assigned_at']),
            models.Index(fields=['doctor']),
        ]

    def __str__(self):
        return f'{self.patient.name} -> {self.doctor.name}'
