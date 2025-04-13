from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings           # Import settings
from django.conf.urls.static import static # Import static
from .views import UserViewSet, MachineViewSet, WarningViewSet, FaultCaseViewSet, FaultNoteViewSet, \
    FaultNoteImageViewSet, FaultCommentViewSet, MachineAssignmentViewSet, WarningCreateAPIView
from .views import fault_report_page
from .views import assigned_machines_api
from . import views
from django.urls import path, include
from .views import index_page, profile_page
from django.contrib.auth.views import LogoutView
from .views import custom_login


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
    path("api/assigned-machines/", assigned_machines_api, name="assigned_machines_api"),
    path('upload-image/', views.upload_fault_image, name='upload_image'),
    path('upload-success/', views.upload_success, name='upload_success'),
    path('', index_page, name='index'),
    path("login/", custom_login, name="custom_login"),
    path("profile/", profile_page, name="profile"),
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
]

# Add this snippet to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
