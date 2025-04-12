from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings

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

    def validate_machine_id(self, value):
        """
        Check that the machine exists AND that it is not already in 'Fault' state.
        """
        try:
            machine = Machine.objects.get(machine_id=value)
            if machine.status == 'Fault':
                raise serializers.ValidationError("Cannot add a warning to a machine that is already in 'Fault' state.")
        except Machine.DoesNotExist:
            raise serializers.ValidationError("Machine with this ID does not exist.")

        return machine

    def create(self, validated_data):
        """
        Create and return a new `Warning` instance, given the validated data.
        """
        machine_id = validated_data['machine_id']
        warning_text = validated_data['warning_text']


        # find the Machine object
        machine = Machine.objects.get(machine_id=machine_id)

        try:
            system_user = User.objects.get(pk=settings.API_SYSTEM_USER_ID)
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
        print("======================================")
        return warning


class FaultCaseCreateSerializer(serializers.Serializer):
    machine_id = serializers.CharField(max_length=12, help_text="The ID of the machine that has faulted.")
    # The initial fault report may only require a text description, with detailed notes to be added later by
    # the technician or repair personnel.
    initial_note_text = serializers.CharField(required=False, allow_blank=True, help_text="Initial notes about the fault.")

    def validate_machine_id(self, value):
        """Check that the machine exists."""
        try:
            machine = Machine.objects.get(machine_id=value)
            # check if it is already fault state
            if machine.status == 'Fault':
                raise serializers.ValidationError("This machine is already in a Fault state.")
        except Machine.DoesNotExist:
            raise serializers.ValidationError("Machine with this ID does not exist.")
        return value

    def create(self, validated_data):
        machine_id = validated_data['machine_id']
        initial_note_text = validated_data.get('initial_note_text', '')

        machine = Machine.objects.get(machine_id=machine_id)

        # --- Find system users  ---
        system_user = None
        try:
            system_user = User.objects.get(pk=settings.API_SYSTEM_USER_ID)
        except (User.DoesNotExist, AttributeError, KeyError):
            raise serializers.ValidationError("System user for API calls not configured or found.")

        # --- create FaultCase object ---
        fault_case = FaultCase.objects.create(
            machine=machine,
            created_by=system_user,
            status='Open' # new fault case is always Open state
        )

        # --- if initial_note_text is not none，create FaultNote ---
        if initial_note_text:
            FaultNote.objects.create(
                fault_case=fault_case,
                user=system_user, # initial note is created by system user
                note_text=initial_note_text
            )

        # --- !! update machine status to Fault !! ---
        machine.status = 'Fault'
        machine.save()

        return fault_case
