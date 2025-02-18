from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    is_admin = models.BooleanField(default=False) 
    groups = models.ManyToManyField(
        Group,
        related_name="expenses_users",  # Change related_name to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="expenses_users_permissions",  # Change related_name to avoid conflict
        blank=True
    )

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Utilities', 'Utilities'),
    ]
    
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100)
    date = models.DateField()
    is_recurring = models.BooleanField(default=False)
    recurrence_period = models.CharField(max_length=50, null=True, blank=True)  # E.g., Daily, Weekly
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.amount}"
