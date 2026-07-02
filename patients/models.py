from django.db import models
from authentication.models import User


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients', db_index=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    medical_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patients'
        unique_together = ['user', 'email']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f'{self.name} ({self.user.email})'
