from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class TargetGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PublishedLocationManager(models.Manager):
    """Custom manager for Location model with filtering methods"""
    
    def by_city(self, city):
        return self.filter(city__iexact=city)
    
    def by_target_group(self, group_name):
        return self.filter(target_group__name__iexact=group_name)


class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    city = models.CharField(max_length=100)
    image = models.ImageField(upload_to='locations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='locations')
    target_group = models.ForeignKey(TargetGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='locations')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='locations_created')
    
    objects = PublishedLocationManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating must be between 1 and 5"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"Review by {self.user.username} on {self.location.name}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'location')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='favorited_by')
    
    def __str__(self):
        return f"{self.user.username} - {self.location.name}"

    class Meta:
        unique_together = ('user', 'location')