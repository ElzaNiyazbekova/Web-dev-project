from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Category, TargetGroup, Location, Review, Favorite
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer,
    CategorySerializer, TargetGroupSerializer, 
    LocationSerializer, ReviewSerializer, FavoriteSerializer
)


# ============================================================================
# FUNCTION-BASED VIEWS (FBVs) - Authentication
# ============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user.
    POST: Create new user account
    Returns: token, user data
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        is_admin = serializer.validated_data.get('is_admin', False)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            is_staff=is_admin,
            is_superuser=is_admin
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'is_admin': user.is_staff,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    User login.
    POST: Authenticate user with username and password
    Returns: token, user data
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'message': 'Logged in successfully'
            }, status=status.HTTP_200_OK)
        return Response({
            'error': 'Invalid username or password'
        }, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    User logout.
    POST: Invalidate user token
    """
    request.user.auth_token.delete()
    return Response({
        'message': 'Logged out successfully'
    }, status=status.HTTP_200_OK)


# ============================================================================
# CLASS-BASED VIEWS (CBVs)
# ============================================================================

class LocationListCreateView(APIView):
    """
    GET: List all locations (supports filtering by category and target_group)
    POST: Create a new location (requires authentication)
    """
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request):
        """List locations with optional filtering"""
        locations = Location.objects.all()
        
        # Filter by category
        category = request.query_params.get('category')
        if category:
            locations = locations.filter(category__name__iexact=category)
        
        # Filter by target_group
        target_group = request.query_params.get('target_group')
        if target_group:
            locations = locations.by_target_group(target_group)
        
        serializer = LocationSerializer(locations, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        """Create a new location"""
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = LocationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDetailView(APIView):
    """
    Full CRUD for individual location:
    GET: Retrieve location details
    PUT: Update location (requires authentication/ownership)
    DELETE: Delete location (requires authentication/ownership)
    """
    
    def get_object(self, pk):
        """Helper to get location or raise 404"""
        return get_object_or_404(Location, pk=pk)
    
    def get(self, request, pk):
        """Retrieve a single location"""
        location = self.get_object(pk)
        serializer = LocationSerializer(location, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Update a location"""
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        location = self.get_object(pk)
        
        # Check ownership (only creator or superuser can edit)
        if location.created_by != request.user and not request.user.is_superuser:
            return Response({
                'error': 'You do not have permission to edit this location'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = LocationSerializer(
            location, data=request.data, partial=True, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Delete a location"""
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        location = self.get_object(pk)
        
        # Check ownership (only creator or superuser can delete)
        if location.created_by != request.user and not request.user.is_superuser:
            return Response({
                'error': 'You do not have permission to delete this location'
            }, status=status.HTTP_403_FORBIDDEN)
        
        location.delete()
        return Response({
            'message': 'Location deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class ReviewListCreateView(APIView):
    """
    GET: List reviews (optionally filtered by location_id)
    POST: Create a new review (requires authentication)
    """
    
    def get(self, request):
        """List reviews, optionally filtered by location"""
        reviews = Review.objects.all()
        
        location_id = request.query_params.get('location_id')
        if location_id:
            reviews = reviews.filter(location_id=location_id)
        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Create a new review"""
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data.copy()
        data['user'] = request.user.id
        
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):
    """
    Handle individual review operations:
    DELETE: Remove a review
    """
    
    def get_object(self, pk):
        return get_object_or_404(Review, pk=pk)
    
    def delete(self, request, pk):
        """Delete a review"""
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        review = self.get_object(pk)
        
        # Check ownership (only creator or superuser can delete)
        if review.user != request.user and not request.user.is_superuser:
            return Response({
                'error': 'You do not have permission to delete this review'
            }, status=status.HTTP_403_FORBIDDEN)
        
        review.delete()
        return Response({
            'message': 'Review deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class FavoriteView(APIView):
    """
    Manage user favorites:
    GET: List current user's favorite locations
    POST: Add location to favorites
    DELETE: Remove location from favorites
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get current user's favorites"""
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        """Add location to favorites"""
        location_id = request.data.get('location_id')
        
        if not location_id:
            return Response({
                'error': 'location_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({
                'error': 'Location not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already favorited
        if Favorite.objects.filter(user=request.user, location=location).exists():
            return Response({
                'error': 'Location already in favorites'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        favorite = Favorite.objects.create(user=request.user, location=location)
        serializer = FavoriteSerializer(favorite, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        """Remove location from favorites"""
        location_id = request.data.get('location_id')
        
        if not location_id:
            return Response({
                'error': 'location_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            favorite = Favorite.objects.get(
                user=request.user,
                location_id=location_id
            )
            favorite.delete()
            return Response({
                'message': 'Removed from favorites'
            }, status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({
                'error': 'Favorite not found'
            }, status=status.HTTP_404_NOT_FOUND)


class CategoryListView(APIView):
    """GET: List all categories"""
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class TargetGroupListView(APIView):
    """GET: List all target groups"""
    
    def get(self, request):
        target_groups = TargetGroup.objects.all()
        serializer = TargetGroupSerializer(target_groups, many=True)
        return Response(serializer.data)
