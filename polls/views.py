from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Machine, FaultCase, FaultNote
from .serializers import MachineSerializer, FaultCaseSerializer, FaultNoteSerializer

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class FaultCaseViewSet(viewsets.ModelViewSet):
    queryset = FaultCase.objects.all()
    serializer_class = FaultCaseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class FaultNoteViewSet(viewsets.ModelViewSet):
    queryset = FaultNote.objects.all()
    serializer_class = FaultNoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
