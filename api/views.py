from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.pagination import PageNumberPagination
from django.views.generic import TemplateView


class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        name=request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email__iexact=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(name=name,email=email, password=password)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email__iexact=email)
            if not user.check_password(password):
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(UserSerializer(user).data)

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return User.objects.filter(Q(email__icontains=query) | Q(name__icontains=query))

    
class FriendRequestThrottle(UserRateThrottle):
    rate = '3/min'

class FriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')
        try:
            to_user = User.objects.get(id=to_user_id)
            if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
                return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
            friend_request = FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

class HandleFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')
        action = request.data.get('action')
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
            if action == 'accept':
                friend_request.status = 'accepted'
            elif action == 'reject':
                friend_request.status = 'rejected'
            friend_request.save()
            return Response(FriendRequestSerializer(friend_request).data)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_400_BAD_REQUEST)

class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            Q(sent_requests__status='accepted', sent_requests__to_user=self.request.user) |
            Q(received_requests__status='accepted', received_requests__from_user=self.request.user)
        ).distinct()

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
