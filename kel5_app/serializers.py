# serializers.py
from rest_framework import serializers
from .models import Project, Projek,ToExperience,Management

class ProyekEngineeringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projek
        fields = '__all__'
        
class ToExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToExperience
        fields = '__all__'
        
class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Management
        fields = '__all__'
        