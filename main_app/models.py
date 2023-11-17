from django.db import models
from django.contrib.auth.models import AbstractUser

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    manager = models.ForeignKey('Manager', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Manager(models.Model):
    user = models.OneToOneField('Employee', on_delete=models.CASCADE, related_name='manager_profile')

    def __str__(self): 
        return self.user.username

class Employee(AbstractUser):
    profile_picture = models.URLField(max_length=200, null=True, blank=True)
    bio = models.TextField(blank=True)
    assigned_groups = models.ManyToManyField(Group, related_name='members', blank=True)
    manager = models.OneToOneField('Manager', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_user')

    def __str__(self):
        return self.username

class Task(models.Model):
    deadline = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey('Manager', on_delete=models.CASCADE, related_name='tasks_created')
    assigned_group = models.OneToOneField('Group', on_delete=models.CASCADE, related_name='task')

    def __str__(self):
        return self.title
