from rest_framework import viewsets, generics, status
from rest_framework.response import Response

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
    return render(request, 'index.html')


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        success_data = {
            "message": "Warning recorded successfully.",
            "status": "success"
        }
        return Response(success_data, status=status.HTTP_201_CREATED)



class FaultCaseCreateAPIView(generics.CreateAPIView):
    """
    API endpoint to create a new FaultCase via POST request.
    Expects JSON data: {"machine_id": "...", "initial_note_text": "..."}
    """
    serializer_class = FaultCaseCreateSerializer

    def create(self, request, *args, **kwargs):
        # 1. get Serializer instance
        serializer = self.get_serializer(data=request.data)
        # 2. validate Serializer，
        serializer.is_valid(raise_exception=True)
        # 3. execute create (call serializer.save() -> serializer.create())
        self.perform_create(serializer)

        # --- 4. if success ---
        success_data = {
            "message": "Fault case created successfully.",
        }
        return Response(success_data, status=status.HTTP_201_CREATED)