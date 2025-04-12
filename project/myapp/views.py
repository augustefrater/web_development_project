from rest_framework import viewsets, generics
from .models import Machine, Warning, FaultCase, FaultNote, FaultNoteImage, FaultComment, MachineAssignment
from .serializers import UserSerializer, MachineSerializer, WarningSerializer, FaultCaseSerializer, FaultNoteSerializer, \
    FaultNoteImageSerializer, FaultCommentSerializer, MachineAssignmentSerializer, WarningCreateSerializer

from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Machine  # make sure your Machine model is defined
from django.shortcuts import render

# ViewSet for User model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class WarningViewSet(viewsets.ModelViewSet):
    queryset = Warning.objects.all()
    serializer_class = WarningSerializer

class FaultCaseViewSet(viewsets.ModelViewSet):
    queryset = FaultCase.objects.all()
    serializer_class = FaultCaseSerializer

class FaultNoteViewSet(viewsets.ModelViewSet):
    queryset = FaultNote.objects.all()
    serializer_class = FaultNoteSerializer

class FaultNoteImageViewSet(viewsets.ModelViewSet):
    queryset = FaultNoteImage.objects.all()
    serializer_class = FaultNoteImageSerializer

class FaultCommentViewSet(viewsets.ModelViewSet):
    queryset = FaultComment.objects.all()
    serializer_class = FaultCommentSerializer

class MachineAssignmentViewSet(viewsets.ModelViewSet):
    queryset = MachineAssignment.objects.all()
    serializer_class = MachineAssignmentSerializer

class WarningCreateAPIView(generics.CreateAPIView):
    """
    API endpoint to create a new Warning via POST request.
    Expects JSON data: {"machine_id": "...", "warning_text": "..."}
    """
    serializer_class = WarningCreateSerializer


def machine_status_api(request):
    machines = Machine.objects.all()
    data = [
        {"id": m.id, "name": m.name, "status": m.status}
        for m in machines
    ]
    return JsonResponse(data, safe=False)

def fault_report_page(request):
    return render(request, 'myapp/fault_report.html')