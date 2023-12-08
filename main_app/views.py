# from django.contrib.auth.models import User, Group
import os
import environ
from .models import *
from .serializers import *
from django.core.mail import send_mail
from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from pathlib import Path

"""
These are settings for .env reader, as well as setting up the exact location from 
where it should read the variables.
"""

env = environ.Env( 
    DEBUG=(bool, False)
)
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [permissions.IsAuthenticated]


class EmployeeRegistration(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeGroupViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGroup.objects.all()
    serializer_class = EmployeeGroupSerializer

    def perform_create(self, serializer):
        manager_id = self.request.data.get('manager')
        serializer.save(manager_id=manager_id)


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    def perform_create(self, serializer):
        serializer.save()
    # permission_classes = [permissions.IsAuthenticated]


class TaskAddViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class TaskDeleteViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
class TaskUpdateViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Check if the user is a manager
#         is_manager = Manager.objects.filter(user=user).exists()

#         # Add custom claim to the token payload
#         token['is_manager'] = is_manager

#         return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtain
    token_obtain_pair = TokenObtainPairView.as_view()
    
class EmailSender(APIView):
    def post(self, request):
        to_email = request.data.get('to')
        subject = request.data.get('subject')
        body = request.data.get('body')
        
        try: 
            email_address = os.environ['GMAIL_USER']
            email_password = os.environ['GMAIL_PASSWORD']
            print(f"EMAIL ADDRESS: {email_address}")
            print(f"EMAIL PASSWORD: {email_password}")
            
            send_mail(
                subject,
                body,
                email_address,
                [to_email],
                fail_silently=False,
                auth_user=email_address,
                auth_password=email_password
            )
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)