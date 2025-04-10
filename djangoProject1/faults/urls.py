from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('create/', views.create_fault_case, name='create_fault_case'),
    path('detail/<int:fault_case_id>/', views.fault_detail, name='fault_detail'),
    # ✅ 新增 dashboard 页面
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('repair/', views.repair_dashboard, name='repair_dashboard'),
    path('resolve/<int:case_id>/', views.mark_as_resolved, name='mark_as_resolved'),
    path('add-machine/', views.add_machine, name='add_machine'),
    path('export-report/', views.export_report, name='export_report'),
    path('testlogout/', lambda request: render(request, 'test_logout.html')),

]

