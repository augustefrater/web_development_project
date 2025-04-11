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


class WarningCreateSerializer(serializers.Serializer):
    machine_id = serializers.CharField(max_length=12, help_text="The ID of the machine experiencing the warning.")
    warning_text = serializers.CharField(help_text="The description of the warning.")

    # validation, Check that the machine exists
    def validate_machine_id(self, value):
        if not Machine.objects.filter(machine_id=value).exists():
            raise serializers.ValidationError("Machine with this ID does not exist.")
        return value

    def create(self, validated_data):
        """
        Create and return a new `Warning` instance, given the validated data.
        """
        machine_id = validated_data['machine_id']
        warning_text = validated_data['warning_text']


        # find the Machine object
        machine = Machine.objects.get(machine_id=machine_id)

        try:
            # system_user = User.objects.get(created_by=created_by)
            system_user = ''
        except User.DoesNotExist:
            raise serializers.ValidationError("System user 'api_system_user' not found.")

        # create Warning object
        warning = Warning.objects.create(
            machine=machine,
            warning_text=warning_text,
            created_by=system_user,
            is_active=True # always true
        )

        if machine.status != 'Fault': # when it's not 'Fault' status
             machine.status = 'Warning'
             machine.save()

        return warning