from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from api.serializer import UserSerializer
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from api.models import User
from rest_framework.response import Response
from dotenv import load_dotenv  
from pathlib import Path
import os
from rest_framework.permissions import IsAuthenticated

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
dotenv_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=dotenv_path)

is_production = True if str(os.environ['is_production']) == '1' else False

# View function for testing server is up or not
@api_view(['GET'])
def test_api(request):

    return JsonResponse({"success":True,"message":"Rentify Server working Fine"},status=status.HTTP_200_OK)


# View function for user registration
@api_view(['POST'])
def signup(request):
    
    print(request.data)
    try:
        serializer = UserSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success':True,'message':'User created successfully!'},status=status.HTTP_201_CREATED)
        
        return JsonResponse({'success':False,'message':'User Creation Failed, Try Agin'},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except IntegrityError as e:
        print(f"Error During User Registration {e}")
        return JsonResponse({'success': False, 'message': 'Username already exists'}, status=status.HTTP_409_CONFLICT)
    
    except Exception as e:
        print(f"Error During User Registration {e}")
        return JsonResponse({'success':False,'message':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# view function for user login 
@csrf_exempt
@api_view(['POST'])
def signin(request):
    
    print(request.data)
    
    try:
        email = request.data['email']
        password = request.data['password']
             
        if not email or not password:
            return JsonResponse({"success":False,"message":"username and password are required"},status = status.HTTP_400_BAD_REQUEST)
          
        # checking the user is exists or not  
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user = authenticate(request, username=user_obj.username, password=password)
               
        if user is not None:
            
            serializer = UserSerializer(user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            response = Response(serializer.data,status = status.HTTP_200_OK)
            print(is_production)
            response.set_cookie('access_token',access_token,httponly=True,secure=is_production,samesite='None')
            return response
        else:
            
            return JsonResponse({"success":False,"message":"Invalid Credentials"},status = status.HTTP_401_UNAUTHORIZED)
        
        
    except Exception as e:
        print(f"Error during User Login {e}")
        return JsonResponse({'success':False,'message':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    

# view function for updating user details
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user(request,id):
    
    try:
    
        try:
            
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            print("Error during user fetching from DB")
            return JsonResponse({"success":False,"message":"User doest not exit"}, status = status.HTTP_404_NOT_FOUND)
        
        # allowing to update partial fields not required all fields to update ---> partial = True
        userSerializer = UserSerializer(user,data = request.data, partial = True) 
        if userSerializer.is_valid():
            
            userSerializer.save()
            return Response(userSerializer.data,status=status.HTTP_200_OK)
        
        return JsonResponse({"success":False,"message":"Invalid data"},status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"Error during User Login {e}")
        return JsonResponse({'success':False,'message':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
    

# view function for delete user account
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request,id):
    
    try:
    
        try:
            
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            print("Error during user fetching from DB")
            return JsonResponse({"success":False,"message":"User doest not exit"}, status = status.HTTP_404_NOT_FOUND)
        
        user.delete()
        
        return JsonResponse({"success":True,"message":"User Account Deleted Successfully"},status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"Error during User Login {e}")
        return JsonResponse({'success':False,'message':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)         
    
    
    

# view function for user logging out
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sign_out(request):
    
    try:
        
        response = Response({"success":True,"message":"User Logged out Successfully"}, status= status.HTTP_200_OK)
        
        response.delete_cookie('access_token')
        
        return response
    
    except Exception as e:
        print(f"Error during User Login {e}")
        return JsonResponse({'success':False,'message':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        