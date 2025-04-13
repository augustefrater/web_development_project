from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.conf import settings           # Import settings
from django.conf.urls.static import static # Import static

from . import views
from .views import UserViewSet, MachineViewSet, WarningViewSet, FaultCaseViewSet, FaultNoteViewSet, \
    FaultNoteImageViewSet, FaultCommentViewSet, MachineAssignmentViewSet, WarningCreateAPIView, FaultCaseCreateAPIView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'warnings', WarningViewSet)
router.register(r'fault-cases', FaultCaseViewSet)
router.register(r'fault-notes', FaultNoteViewSet)
router.register(r'fault-note-images', FaultNoteImageViewSet)
router.register(r'fault-comments', FaultCommentViewSet)
router.register(r'machine-assignments', MachineAssignmentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    #path('', views.index_view, name='index'),
    path('api/external/warnings/create/', WarningCreateAPIView.as_view(), name='api_external_warning_create'),
    path('api/external/faults/create/', FaultCaseCreateAPIView.as_view(), name='api_external_fault_create'),
    
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('fault-report/', TemplateView.as_view(template_name='fault-report.html'), name='fault-report'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('signup/', TemplateView.as_view(template_name='signup.html'), name='signup'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
