from rest_framework import serializers
from .models import Project
from user.serializer import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):

    project_owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.project_name = validated_data.get(
            'project_name', instance.project_name)
        instance.project_description = validated_data.get(
            'project_description', instance.project_description)
        instance.save()
        return instance
