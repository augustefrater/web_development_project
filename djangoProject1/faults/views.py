from django.shortcuts import render
from .forms import MachineForm

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FaultCaseForm
from .models import FaultCase, FaultImage
from django.contrib.auth.decorators import login_required

@login_required
def create_fault_case(request):
    if request.method == 'POST':
        form = FaultCaseForm(request.POST)
        files = request.FILES.getlist('images')
        if form.is_valid():
            fault_case = form.save(commit=False)
            fault_case.created_by = request.user
            fault_case.save()
            for file in files:
                FaultImage.objects.create(fault_case=fault_case, image=file)
            return redirect('fault_detail', fault_case.id)
    else:
        form = FaultCaseForm()
    return render(request, 'create_fault_case.html', {'form': form})

@login_required
def fault_detail(request, fault_case_id):
    fault_case = get_object_or_404(FaultCase, pk=fault_case_id)
    return render(request, 'fault_detail.html', {'fault_case': fault_case})
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def repair_dashboard(request):
    if request.user.profile.role != "Repair":
        return redirect('/faults/dashboard/')  # 只允许 Repair 访问

    unresolved_cases = FaultCase.objects.exclude(status='Resolved')

    return render(request, 'repair_dashboard.html', {
        'cases': unresolved_cases
    })

@login_required
def mark_as_resolved(request, case_id):
    if request.user.profile.role != "Repair":
        return redirect('/faults/dashboard/')

    case = get_object_or_404(FaultCase, id=case_id)
    case.status = 'Resolved'
    case.save()
    return redirect('repair_dashboard')

@login_required
def add_machine(request):
    if request.user.profile.role != "Manager":
        return redirect('/faults/dashboard/')

    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MachineForm()
    return render(request, 'add_machine.html', {'form': form})

import csv
from django.http import HttpResponse

from .models import FaultCase

@login_required
def export_report(request):
    if request.user.profile.role != "Manager":
        return redirect('/faults/dashboard/')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fault_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['标题', '描述', '状态', '创建人', '创建时间'])

    for case in FaultCase.objects.all():
        writer.writerow([
            case.title,
            case.description,
            case.status,
            case.created_by.username,
            case.created_at.strftime('%Y-%m-%d %H:%M')
        ])

    return response
