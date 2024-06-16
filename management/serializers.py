from rest_framework import serializers
from .models import Project, Task, Comment

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
    def validate(self, data):
        if 'name' not in data or 'description' not in data:
            raise serializers.ValidationError("Both name and description are required.")
        return data

class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    class Meta:
        model = Task
        fields = '__all__'
    def validate_due_date(self, value):
        if value is None:
            raise serializers.ValidationError("The due_date field is required.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    class Meta:
        model = Comment
        fields = '__all__'