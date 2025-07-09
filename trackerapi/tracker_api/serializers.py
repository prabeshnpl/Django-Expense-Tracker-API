from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ExpenseIncome

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
            
class ExpenseIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseIncome
        fields = '__all__'

        