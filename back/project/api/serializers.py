from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, TargetGroup, Location, Review, Favorite


# ============================================================================
# USER SERIALIZERS
# ============================================================================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# ============================================================================
# PLAIN SERIALIZERS (non-model)
# ============================================================================

class LoginSerializer(serializers.Serializer):
    """Serializer for login endpoint"""
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})


class RegisterSerializer(serializers.Serializer):
    """Serializer for registration endpoint"""
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    is_admin = serializers.BooleanField(required=False, default=False)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password": "Passwords don't match"
            })
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({
                "username": "Username already exists"
            })
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                "email": "Email already exists"
            })
        return data


# ============================================================================
# MODEL SERIALIZERS
# ============================================================================

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TargetGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetGroup
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'text', 'rating', 'user', 'location', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class LocationSerializer(serializers.ModelSerializer):
    """Main Location serializer with nested relations and computed rating"""
    category = CategorySerializer(read_only=True)
    target_group = TargetGroupSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=True)
    target_group_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    def get_rating(self, obj):
        """Calculate average rating from all reviews"""
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        avg_rating = sum(r.rating for r in reviews) / reviews.count()
        return round(avg_rating, 1)

    def get_review_count(self, obj):
        """Count total reviews"""
        return obj.reviews.count()

    class Meta:
        model = Location
        fields = [
            'id', 'name', 'description', 'city', 'image',
            'category', 'category_id',
            'target_group', 'target_group_id',
            'created_by', 'created_at',
            'reviews', 'rating', 'review_count'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'reviews', 'rating', 'review_count']

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        target_group_id = validated_data.pop('target_group_id', None)
        
        category = Category.objects.get(id=category_id)
        target_group = TargetGroup.objects.get(id=target_group_id) if target_group_id else None
        
        location = Location.objects.create(
            category=category,
            target_group=target_group,
            created_by=self.context['request'].user,
            **validated_data
        )
        return location

    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        target_group_id = validated_data.pop('target_group_id', None)
        
        if category_id:
            instance.category = Category.objects.get(id=category_id)
        if target_group_id is not None:
            instance.target_group = TargetGroup.objects.get(id=target_group_id)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        """Customize the output to return absolute image URLs"""
        data = super().to_representation(instance)
        if data.get('image') and self.context.get('request'):
            data['image'] = self.context['request'].build_absolute_uri(data['image'])
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'location', 'location_id']
        read_only_fields = ['id', 'user']
