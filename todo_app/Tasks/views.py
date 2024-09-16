from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from .models import Task, User
from .forms import TaskForm, UserCreationForm
from .forms import ConfirmDeleteForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

def index(request):
    return render(request, "index.html",{})


@login_required
def task_lists(request):
    if request.user.is_superuser:
        tasks = Task.objects.all().order_by("-created")
    # Handles the display of tasks to the logged-in user.
    # The user will only see tasks that are either assigned to them or created by them.
    else:
        tasks = (Task.objects.filter(assigned_to=request.user) | Task.objects.filter(created_by=request.user)).distinct().order_by("-created")
    return render(request, "task_list.html", {"tasks": tasks})

# class TaskList(ListView, LoginRequiredMixin):
#     model = Task
#     template_name = "task_list.html"

#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return Task.objects.all().order_by("-created")
#         else:
#             return Task.objects.filter(assigned_to=self.request.user) | Task.objects.filter(created_by=self.request.user).distinct().order_by("-created")
    
    
class UserList(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = User
    form_class = UserCreationForm
    template_name = "user_list.html"
    
    def test_func(self):
        return self.request.user.is_superuser

    

class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "create_task.html"

    def get_success_url(self):
        return reverse("tasks")
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    # def test_func(self):
    #     return self.request.user.is_superuser
# @login_required
# def create_task(request):
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             # Create a new Task object from the form data without saving it to the database yet
#             task = form.save(commit=False)
#             # Set the `created_by` field of the task to the current user
#             task.created_by = request.user
#             task.save()
#             #The reverse function is used to resolve the URL name 'tasks' into its corresponding URL path.
#             return HttpResponseRedirect(reverse('tasks'))
#     else:
#         form = TaskForm()
#     return render(request, "create_task.html", {"form": form})

# @permission_required("can_edit_task")
# def update_task(request, task_id):
#     try:
#         task = Task.objects.get(id=task_id)
#     except Task.DoesNotExist:
#         raise Http404("Task does not exist")

#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('tasks')
#     else:
#         form = TaskForm(instance=task)
#     return render(request, 'task_update.html', {"form": form})

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_update.html"

    def get_success_url(self):
        return reverse("tasks")
    
    def test_func(self):
        task = self.get_object()
        return self.request.user == task.created_by or self.request.user.is_superuser
        
# @permission_required("can_delete_task")        
# def delete_task(request, task_id):
#     task = Task.objects.get(id=task_id)
#     if request.method == 'POST':
#         form = ConfirmDeleteForm(request.POST)
#         if form.is_valid():
#             task.delete()
#             return redirect('tasks')
#     else:
#         form = ConfirmDeleteForm()
#     return render(request, 'confirm_delete.html', {"form": form})
class DeleteTaskView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Task
    form_class = ConfirmDeleteForm
    template_name = "confirm_delete.html"

    def get_success_url(self):
        return reverse("tasks")
    
    def test_func(self):
        task = self.get_object()
        return self.request.user == task.created_by or self.request.user.is_superuser

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
            print(form.errors)
    else:
        form=UserCreationForm
    return render(request, 'register.html', {"form": form})