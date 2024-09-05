from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskListView, LoginView, LogoutView, TaskUpdateView, DeleteView
from Tasks.models import Task
from .serializers import TaskSerializer, LoginSerializer, LogoutSerializer
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('tasklist', TaskListView, basename='taklist')

urlpatterns = [
    path('view_create', TaskListView.as_view (queryset=Task.objects.all(), serializer_class = TaskSerializer)),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('login/', LoginView.as_view(queryset=Task.objects.all(), serializer_class = LoginSerializer)),
    path('logout/', LogoutView.as_view(queryset=Task.objects.all(), serializer_class = LogoutSerializer)),
    path('deletetask/<int:pk>/', DeleteView.as_view(queryset=Task.objects.all(), serializer_class = TaskSerializer)),
    path('updatetask/<int:pk>/', TaskUpdateView.as_view(queryset=Task.objects.all(), serializer_class = TaskSerializer)),
]
