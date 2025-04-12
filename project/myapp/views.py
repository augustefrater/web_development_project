from rest_framework import viewsets, generics
from rest_framework.response import Response  # ✅ Required to return custom API responses
from rest_framework.permissions import IsAuthenticated  # ✅ Ensures user must be logged in
from rest_framework.decorators import api_view, permission_classes  # ✅ For function-based API views with DRF

from django.contrib.auth.decorators import login_required  # ✅ For protecting HTML views
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from .models import Machine, Warning, FaultCase, FaultNote, FaultNoteImage, FaultComment, MachineAssignment
from .serializers import (
    UserSerializer, MachineSerializer, WarningSerializer, FaultCaseSerializer, FaultNoteSerializer,
    FaultNoteImageSerializer, FaultCommentSerializer, MachineAssignmentSerializer, WarningCreateSerializer
)

# 🔧 API ViewSets (DRF auto-generates endpoints like /api/users/, etc.)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class WarningViewSet(viewsets.ModelViewSet):
    queryset = Warning.objects.all()
    serializer_class = WarningSerializer

# 🛠️ Fault cases – authenticated users can create new fault reports
class FaultCaseViewSet(viewsets.ModelViewSet):
    queryset = FaultCase.objects.all()
    serializer_class = FaultCaseSerializer
    permission_classes = [IsAuthenticated]  # ✅ Only logged-in users can access

    def create(self, request, *args, **kwargs):
        print("📥 Incoming raw data:", request.data)
        print("🔐 Authenticated user:", request.user)

        if not request.user.is_authenticated:
            print("❌ User is NOT authenticated")

        # No need to pass created_by manually — we’ll inject the user in serializer.save()
        mutable_data = request.data.copy()
        serializer = self.get_serializer(data=mutable_data)

        if not serializer.is_valid():
            print("❌ Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=400)

        # ✅ Automatically assign the logged-in user
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)

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

# 🚨 Endpoint to create warnings externally
class WarningCreateAPIView(generics.CreateAPIView):
    serializer_class = WarningCreateSerializer

# 📊 View to display all machine statuses (if needed)
def machine_status_api(request):
    machines = Machine.objects.all()
    data = [
        {"id": m.id, "name": m.name, "status": m.status}
        for m in machines
    ]
    return JsonResponse(data, safe=False)

# 🛡️ Fault reporting HTML page – protected so only logged-in users can see it
@login_required
def fault_report_page(request):
    return render(request, 'myapp/fault_report.html')

# 🔐 API to fetch machines assigned to the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def assigned_machines_api(request):
    user = request.user  # ✅ Get the logged-in user from the session
    print("👤 Assigned machine request for:", user.username)

    # Get only assignments for this user
    assignments = MachineAssignment.objects.filter(user=user).select_related("machine")

    # Convert assigned machines into JSON format
    machines = [
        {
            "machine_id": a.machine.machine_id,
            "name": a.machine.name,
            "status": a.machine.status
        }
        for a in assignments
    ]

    return JsonResponse(machines, safe=False)