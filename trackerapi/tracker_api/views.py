from rest_framework.response import Response 
from rest_framework.views import APIView 
from .serializers import UserSerializer, ExpenseIncomeSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import ExpenseIncome

# Create your views here.

class Login(APIView):
    def get(self,request):
        print(request.user.is_authenticated)
        if 'logged_in' not in request.session:
            logout(request)
        if request.user.is_authenticated:
            return Response({'message': "You are already logged in","user":request.user.username})    
        return Response({'message':"Please Login"})

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request,auth_user)
                if 'logged_in' not in request.session:
                    request.session['logged_in'] = True
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

class Expenses(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self,request,pk=None):
        user = request.user 
        if not user.is_authenticated:
            return Response({"User not authenticated"})
        try:
            if pk:
                expense = ExpenseIncome.objects.get(pk=pk,user=user)            
                serializer = ExpenseIncomeSerializer(expense)
                if serializer.is_valid():
                    return Response(serializer.data)
                else:
                    return Response({'Error': 'Invalid data'}, status=400)
            else:                          
                expenses = ExpenseIncome.objects.filter(user=user)
                serializer = ExpenseIncomeSerializer(expenses,many=True)
                if serializer.is_valid():
                    return Response(serializer.data)
                else:
                    return Response({'Message':'Error Occured'},status=404)
        except Exception as e:
            return Response({'Error':str(e)})
        
    
