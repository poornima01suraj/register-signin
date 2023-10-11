from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import CustomUser
from .serializers import UserSignInSerializer
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        web_terms = request.data.get('web_terms')
        dataprocessing = request.data.get('dataprocessing')
        subscription = request.data.get('subscription')

        if not any([username]):
            return Response({'error': 'Please provide at least one of username, email, or phone_number'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(password)
        existing_user = CustomUser.objects.filter(
        Q(username__iexact=username) |
        Q(email__iexact=username)
        ).exists()

    

        if existing_user:
            return Response({'error': 'Username, email, or phone_number already exists'}, status=status.HTTP_409_CONFLICT)

        # Create a new user
        user = CustomUser.objects.create(
            username=username,
            password=hashed_password,
            web_terms=web_terms,
            dataprocessing=dataprocessing,
            subscription=subscription
        )
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def signin(request):
    if request.method == 'POST':
        identifier = request.data.get('identifier')
        password = request.data.get('password')
        
        if identifier is None or password is None:
            return Response({'error': 'Both identifier and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(username=identifier).first()

        if user and user.check_password(password):
            return Response({'message': 'Signin successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)














