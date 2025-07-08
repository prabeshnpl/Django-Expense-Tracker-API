from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ExpenseIncome(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    transaction_types = models.CharField(choices=['credit', 'debit'])
    tax = models.DecimalField(default=0)
    tax_type = models.CharField(choices=['flat','percentage'],default='flat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
