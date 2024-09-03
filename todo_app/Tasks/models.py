from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [("can_edit_task", "Can Edit Task"),
                       ("can_delete_task", "Can Delete Task")]