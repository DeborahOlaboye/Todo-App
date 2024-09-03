from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from Tasks.models import Task
from .serializers import TaskSerializer
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        else:
            return Task.objects.filter(assigned_to=self.request.user) | Task.objects.filter(created_by=self.request.user).distinct().order_by("-created")
        
class DeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("index")