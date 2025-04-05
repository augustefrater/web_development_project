from rest_framework import viewsets
from .models import User, Machine, Warning, FaultCase, FaultNote, FaultNoteImage, FaultComment, MachineAssignment
from .serializers import UserSerializer, MachineSerializer, WarningSerializer, FaultCaseSerializer, FaultNoteSerializer, FaultNoteImageSerializer, FaultCommentSerializer, MachineAssignmentSerializer

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
