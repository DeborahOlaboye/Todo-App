from django.contrib import admin
from .models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'assigned_to')
    list_filter = ('created_by', 'assigned_to')
admin.site.register(Task, TaskAdmin)
