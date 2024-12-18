from datetime import datetime
from .serializers import UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login
from .serializers import *
from rest_framework import generics, status
from .models import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Count





# userregistration endpoint
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Add user to a group
        group = self.get_or_create_group()
        group.members.add(user)
        group.save()

        group_members = group.members.all()  
        other_members = [{'id': member.id, 'username': member.username, 'email': member.email} for member in group_members]


        response_data = {
            'user': serializer.data,
            'message': 'Registration successful. Please log in.',
            'group': {
                'name': group.name,
                'other_members': other_members,
                'is_full': group.members.count() >= 4
            }
        }

        # Ensure a proper Response is returned
        return Response(response_data, status=201)

    def get_or_create_group(self):
        
        
        group = (
            UserGroup.objects.annotate(member_count=Count('members'))
            .filter(member_count__lt=4)
            .first()
        )

        
        if not group:
            group_name = f"Group {UserGroup.objects.count() + 1}"
            group = UserGroup.objects.create(name=group_name)

        return group
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Paymenet Gateway:





