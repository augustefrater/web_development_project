from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    Machine, Warning, FaultCase,
    FaultNote, FaultNoteImage, FaultComment,
    MachineAssignment
)

# Converts User instances to JSON and validates incoming data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Include all fields from the User model

# Useful for listing machines and creating/updating them via API
class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'  # Include all fields from the Machine model

# Handles warnings related to machines
class WarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warning
        fields = '__all__'

# Represents a machine fault case including its status and resolution
class FaultCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultCase
        fields = '__all__'

# Handles internal notes made about a fault case
class FaultNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultNote
        fields = '__all__'

# Deals with images attached to a fault note (binary data)
class FaultNoteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultNoteImage
        fields = '__all__'

# Represents comments made on a fault case by users
class FaultCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultComment
        fields = '__all__'

# Manages assignment of users to machines for specific roles
class MachineAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineAssignment
        fields = '__all__'