from django.contrib.auth import authenticate, login

from .serializers import RegistrationSerializer , AssignmentSerializer
from doc_app.models import Assignment , CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def custom_auth_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate user
    user = authenticate(username=username, password=password)

    if user is not None:
        # Log the user in
        login(request, user)
        
        # Return user details
        return Response({
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type
        })
    else:
        # Return error if authentication fails
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()

@csrf_exempt
@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        
        data['username'] = account.username
        data['email'] = account.email
        data['user_type'] = account.user_type
        data['id'] = account.id
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


#view to create assignemnt 

@csrf_exempt
@api_view(['POST'])
def create_assignment(request):
    try:
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#view to get all the assignments
@csrf_exempt
@api_view(['GET'])
def get_assignments(request):
    try:
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#view to get the assignment by id
@csrf_exempt
@api_view(['GET'])
def get_assignment(request, pk):
    try:
        assignment = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return Response({'error': 'Assignment does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = AssignmentSerializer(assignment)
    return Response(serializer.data)
