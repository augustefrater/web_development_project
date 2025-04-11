from rest_framework import viewsets, generics
from .models import Machine, Warning, FaultCase, FaultNote, FaultNoteImage, FaultComment, MachineAssignment
from .serializers import UserSerializer, MachineSerializer, WarningSerializer, FaultCaseSerializer, FaultNoteSerializer, \
    FaultNoteImageSerializer, FaultCommentSerializer, MachineAssignmentSerializer, WarningCreateSerializer, \
    FaultCaseCreateSerializer

from django.contrib.auth.models import User
from django.shortcuts import render


def index_view(request):
    context = {
        'page_title': 'Factory Status Home',
    }
    return render(request, 'myapp/index2.html', context)


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

class FaultCaseCreateAPIView(generics.CreateAPIView):
    """
    API endpoint to create a new FaultCase via POST request.
    Expects JSON data: {"machine_id": "...", "initial_note_text": "..."}
    """
    serializer_class = FaultCaseCreateSerializer