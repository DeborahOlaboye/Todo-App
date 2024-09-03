from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskListView, LoginView, LogoutView, TaskUpdateView, DeleteView
from Tasks.models import Task
from .serializers import TaskSerializer

router = DefaultRouter()
router.register('tasklist', TaskListView, basename='taklist')

urlpatterns = [
    path('', TaskListView.as_view (queryset=Task.objects.all(), serializer_class = TaskSerializer)),
    path('login', LoginView.as_view(), name='api_login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('deletetask/<int:pk>/', DeleteView.as_view(queryset=Task.objects.all(), serializer_class = TaskSerializer)),
    path('updatetask/<int:pk>/', DeleteView.as_view(queryset=Task.objects.all(), serializer_class = TaskSerializer)),
]
