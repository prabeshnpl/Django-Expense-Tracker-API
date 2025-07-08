from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ExpenseIncome(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)

    TRANSACTION_TYPES_CHOICES = [
        ('credit','Credit'),
        ('debit','Debit'),
    ]
    transaction_types = models.CharField(choices=TRANSACTION_TYPES_CHOICES)
    tax = models.DecimalField(default=0,max_digits=10,decimal_places=2)

    TAX_TYPE_CHOICES = [
        ('flat', 'Flat'),
        ('percentage', 'Percentage'),
    ]

    tax_type = models.CharField(max_length=20, choices=TAX_TYPE_CHOICES, default='flat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
