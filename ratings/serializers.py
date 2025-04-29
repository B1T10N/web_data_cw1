from rest_framework import serializers
from .models import Professor, Module, ModuleInstance, Rating
from django.contrib.auth.models import User

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['professor_id', 'name']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['module_code', 'module_name']

class ModuleInstanceSerializer(serializers.ModelSerializer):
    professors = ProfessorSerializer(many=True)

    class Meta:
        model = ModuleInstance
        fields = ['module', 'year', 'semester', 'professors']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'professor', 'module_instance', 'rating']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
