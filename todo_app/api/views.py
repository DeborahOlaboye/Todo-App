from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from Tasks.models import Task
from .serializers import TaskSerializer
from rest_framework import generics
from django.http import HttpResponse, HttpResponseRedirect
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
            return Task.objects.filter(assigned_to=user) | Task.objects.filter(created_by=user).distinct().order_by("-created")

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            raise PermissionDenied("You do not have permission to update tasks.")
        return super().update(request, *args, **kwargs)
        
class DeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginView(generics.GenericAPIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message:" "Login Successful"})
        else:
            return Response({"message:" "Invalid username or password"})

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return redirect("index")