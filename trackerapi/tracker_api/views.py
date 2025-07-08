from django.shortcuts import redirect
from rest_framework.response import Response 
from rest_framework.views import APIView 
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class Login(APIView):
    def get(self,request):
        return Response({'message':"Please Login"})
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            print(username,password)
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request,auth_user)
                return Response({'message': 'Login successful !! You are now logged in','Hint':'You can now redirect to your api dashboard manually by altering endpoints in url.'},status=200)
            else:
                return Response({'message': 'Invalid credentials'}, status=400)
        else:
            return Response({"Message":f"Unexpected error"})
        
class Register(APIView):
    def get(self,request):
        return Response({'message':'Please Register'})
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Registration successful'})
        else:
            return Response({"Message":f"{serializer.errors}"})

# class 
