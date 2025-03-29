from rest_framework import serializers
from .models import Machine, FaultCase, FaultNote, User

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'

class FaultCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultCase
        fields = '__all__'

class FaultNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultNote
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
