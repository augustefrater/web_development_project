from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.conf import settings           # Import settings
from django.conf.urls.static import static # Import static
from .views import UserViewSet, MachineViewSet, WarningViewSet, FaultCaseViewSet, FaultNoteViewSet, \
    FaultNoteImageViewSet, FaultCommentViewSet, MachineAssignmentViewSet, WarningCreateAPIView
from .views import fault_report_page

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
    path('api/external/warnings/create/', WarningCreateAPIView.as_view(), name='api_external_warning_create'),
    path('report-fault/', fault_report_page, name='fault_report'),
]

# Add this snippet to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
