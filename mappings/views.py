from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = Patient.objects.filter(id=request.data.get('patient'), user=request.user)
        if not patient.exists():
            return Response(
                {'error': 'Patient not found or does not belong to you.'},
                status=status.HTTP_404_NOT_FOUND
            )

        self.perform_create(serializer)
        return Response(
            {'message': 'Doctor assigned successfully.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        mappings = self.get_queryset().filter(patient_id=patient_id)
        serializer = self.get_serializer(mappings, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(
            {'message': 'Doctor assignment removed successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
