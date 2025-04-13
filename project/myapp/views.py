from rest_framework import viewsets, generics
from rest_framework.response import Response  # Required to return custom API responses
from rest_framework.permissions import IsAuthenticated  # Ensures user must be logged in
from rest_framework.decorators import api_view, permission_classes  # For function-based API views with DRF
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # For protecting HTML views
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
# Models and forms
from .models import Machine, Warning, FaultCase, FaultNote, FaultNoteImage, FaultComment, MachineAssignment
from .forms import FaultNoteImageForm
from django.contrib import messages
# Serializers
from .serializers import (
    UserSerializer, MachineSerializer, WarningSerializer, FaultCaseSerializer, FaultNoteSerializer,
    FaultNoteImageSerializer, FaultCommentSerializer, MachineAssignmentSerializer, WarningCreateSerializer
)

# Index/Home page
def index_page(request):
    return render(request, 'myapp/index.html')

# Profile page
@login_required
def profile_page(request):
    return render(request, 'myapp/profile.html')

# Fault report page (requires login)
@login_required
def fault_report_page(request):
    return render(request, 'myapp/fault_report.html')

@login_required
def dashboard_page(request):
    # Obtener todas las máquinas
    machines = Machine.objects.all()

    # Contar estados
    total_machines = machines.count()
    online_count = machines.filter(status="OK").count()
    offline_count = machines.filter(status="Warning").count()
    maintenance_count = machines.filter(status="Fault").count()

    # Obtener las 5 máquinas más recientemente actualizadas (si tienes un campo como 'last_updated')
    latest_machines = machines.order_by('-machine_id')[:5]

    context = {
        "total_machines": total_machines,
        "online_count": online_count,
        "offline_count": offline_count,
        "maintenance_count": maintenance_count,
        "latest_machines": latest_machines,
    }

    return render(request, 'myapp/dashboard.html', context)

# Upload success page
def upload_success(request):
    return render(request, 'myapp/upload_success.html')

# Optional: handle manual image upload form
def upload_fault_image(request):
    if request.method == 'POST':
        form = FaultNoteImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else:
        form = FaultNoteImageForm()
    return render(request, 'myapp/upload_image.html', {'form': form})

# Assigned machines API for current logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def assigned_machines_api(request):
    user = request.user
    print("👤 Assigned machine request for:", user.username)
    assignments = MachineAssignment.objects.filter(user=user).select_related("machine")

    machines = [
        {
            "machine_id": a.machine.machine_id,
            "name": a.machine.name,
            "status": a.machine.status
        }
        for a in assignments
    ]
    return JsonResponse(machines, safe=False)

# View to return machine statuses (if needed)
def machine_status_api(request):
    machines = Machine.objects.all()
    data = [
        {"id": m.id, "name": m.name, "status": m.status}
        for m in machines
    ]
    return JsonResponse(data, safe=False)

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username} 👋') 
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, "myapp/registration/login.html")
# 🔧 DRF ViewSets below:
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
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("Incoming raw data:", request.data)
        print("Authenticated user:", request.user)
        mutable_data = request.data.copy()
        serializer = self.get_serializer(data=mutable_data)

        if not serializer.is_valid():
            print("❌ Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=400)

        serializer.save(created_by=request.user)
        return Response(serializer.data, status=201)

class FaultNoteViewSet(viewsets.ModelViewSet):
    queryset = FaultNote.objects.all()
    serializer_class = FaultNoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

class FaultNoteImageViewSet(viewsets.ModelViewSet):
    queryset = FaultNoteImage.objects.all()
    serializer_class = FaultNoteImageSerializer

    def create(self, request, *args, **kwargs):
        print("Incoming image upload:", request.data)
        print("Files:", request.FILES)
        return super().create(request, *args, **kwargs)

class FaultCommentViewSet(viewsets.ModelViewSet):
    queryset = FaultComment.objects.all()
    serializer_class = FaultCommentSerializer

class MachineAssignmentViewSet(viewsets.ModelViewSet):
    queryset = MachineAssignment.objects.all()
    serializer_class = MachineAssignmentSerializer

class WarningCreateAPIView(generics.CreateAPIView):
    serializer_class = WarningCreateSerializer

