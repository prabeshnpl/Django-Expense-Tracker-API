from rest_framework.serializers import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.Modelserializer):
    class Meta:
        model = User
        fields = '__all__'
        