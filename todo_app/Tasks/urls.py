from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CreateTaskView, TaskUpdateView, DeleteTaskView, UserList
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasklist', views.task_lists, name = 'tasks'),
    path('createtask', CreateTaskView.as_view(template_name='create_task.html'), name = 'create_task'),
    path('updatetask/<int:pk>/', TaskUpdateView.as_view(template_name = "task_update.html"), name = 'update_task'),
    path('deletetask/<int:pk>/', DeleteTaskView.as_view(template_name = "confirm_delete.html"), name = 'delete_task'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('userlist', UserList.as_view(template_name = "user_list.html"), name = 'userlist'),
]