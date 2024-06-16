from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

class ProjectView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        
        if pk:
            cache_key = f'project_{pk}'
            project = cache.get(cache_key)
            if not project:
                project = get_object_or_404(Project, pk=pk)
                cache.set(cache_key, project, timeout=3600)  
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        cache_key = 'projects'
        projects = cache.get(cache_key)
        if not projects:
            projects = Project.objects.all()
            cache.set(cache_key, projects, timeout=3600)  
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            cache_key = f'project_{project.pk}'
            cache.delete(cache_key)  
            cache.delete('projects')  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache_key = f'project_{pk}'
            cache.delete(cache_key)  
            cache.delete('projects')  
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        cache_key = f'project_{pk}'
        cache.delete(cache_key)  
        cache.delete('projects')  
        return Response(status=status.HTTP_204_NO_CONTENT)



class TaskView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            cache_key = f'task_{pk}'
            task = cache.get(cache_key)
            if not task:
                task = get_object_or_404(Task, pk=pk)
                serializer = TaskSerializer(task)
                cache.set(cache_key, task, timeout=3600)  
            else:
                serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        cache_key = 'tasks'
        tasks = cache.get(cache_key)
        if not tasks:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            cache.set(cache_key, tasks, timeout=3600) 
        else:
            serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            cache.delete('tasks')  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'task_{pk}') 
            cache.delete('tasks')  
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        cache.delete(f'task_{pk}')  
        cache.delete('tasks') 
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentsView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f'comments_for_task_{pk}'
        comments = cache.get(cache_key)
        if not comments:
            task = get_object_or_404(Task, pk=pk)
            comments = Comment.objects.filter(task=task)
            serializer = CommentSerializer(comments, many=True)
            cache.set(cache_key, serializer.data, timeout=3600)  
        else:
            serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        request.data['task'] = task.id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'comments_for_task_{task_id}')  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)