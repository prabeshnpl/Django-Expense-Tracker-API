from rest_framework.response import Response 
from rest_framework.views import APIView 
from .serializers import UserSerializer, ExpenseIncomeSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import ExpenseIncome
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class Login(APIView):
    def get(self,request):
        if 'logged_in' not in request.session:
            logout(request)
        if request.user.is_authenticated:
            return Response({'message': "You are already logged in","user":request.user.username})    
        return Response({'message':"Please Login"})

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request=request,user=user)
                refresh = RefreshToken.for_user(user)
                if 'logged_in' not in request.session:
                    request.session['logged_in'] = True
                    request.session['refresh'] = str(refresh)
                    request.session['access'] = str(refresh.access_token)
                return Response({'message': 'Login successful !! You are now logged in','refresh':str(refresh),"access":str(refresh.access_token)},status=200)
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

class Logout(APIView):
    def get(self,request):
        logout(request)
        return Response({"Logged Out Successfully!!"})

class Expenses(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        user = request.user               
        if not user.is_authenticated:
            return Response({"User not authenticated"})
        try:
            if pk:
                expense = ExpenseIncome.objects.get(pk=pk,user=user)            
                serializer = ExpenseIncomeSerializer(expense)
                type = serializer.data.get('tax_type')
                amount = float(serializer.data.get('amount'))
                tax = float(serializer.data.get('tax'))
                if type == 'flat':
                    total = amount + (tax)
                else:
                    total = amount + tax * amount / 100
                data = serializer.data.copy()
                data['total'] = total
                return Response(data)
            else:                          
                expenses = ExpenseIncome.objects.filter(user=user).order_by('-created_at')
                paginator = PageNumberPagination()
                pagianted_expenses = paginator.paginate_queryset(expenses,request)
                serializer = ExpenseIncomeSerializer(pagianted_expenses, many=True)
                data = serializer.data
                for item in data:
                    item.pop('updated_at', None)
                    item.pop('tax', None)
                    item.pop('tax_type', None)
                    item.pop('description', None)
                return paginator.get_paginated_response(data)
        except Exception as e:
            return Response({'Error':str(e)})
        
    def post(self,request):
        data = request.data
        data['user'] = request.user.pk
        serializer = ExpenseIncomeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors)
    
    def delete(self,request,pk=None):
        if not pk:
            return Response({"Message":"Can't delete all message at once!!"})
        item = ExpenseIncome.objects.get(pk=pk,user=request.user)
        item.delete()
        return Response({"Deleted Successfully"},status=204)

    def put(self,request,pk=None):
        if not pk:
            return Response({"Please Select the object through 'pk'"})
        item = ExpenseIncome.objects.get(pk=pk,user=request.user)
        serializer = ExpenseIncomeSerializer(item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Updated Successfully"},status=200)
        else:
            return Response(serializer.errors)
