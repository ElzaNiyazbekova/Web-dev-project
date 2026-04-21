from django.contrib import admin
from .models import Category, TargetGroup, Location, Review, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(TargetGroup)
class TargetGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'category', 'target_group', 'created_by', 'created_at']
    list_filter = ['category', 'target_group', 'created_at', 'city']
    search_fields = ['name', 'description', 'city']
    readonly_fields = ['created_at', 'created_by']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'city', 'image')
        }),
        ('Classification', {
            'fields': ('category', 'target_group')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user', 'get_location', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'location']
    search_fields = ['text', 'user__username', 'location__name']
    readonly_fields = ['created_at', 'user']
    
    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'
    
    def get_location(self, obj):
        return obj.location.name
    get_location.short_description = 'Location'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user', 'get_location']
    list_filter = ['user']
    search_fields = ['user__username', 'location__name']
    
    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'
    
    def get_location(self, obj):
        return obj.location.name
    get_location.short_description = 'Location'
