from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MachineViewSet, WarningViewSet, FaultCaseViewSet, FaultNoteViewSet, FaultNoteImageViewSet, FaultCommentViewSet, MachineAssignmentViewSet

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
]
