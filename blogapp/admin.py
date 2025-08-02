from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import slugify
from .models import Post, Category, Tag, Comment, Newsletter, Contact

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'post_count', 'color_preview')
    list_editable = ('color',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Posts'
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; display: inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Posts'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'rating', 'views', 'created_at', 'author')
    list_filter = ('status', 'category', 'anime_type', 'created_at', 'rating')
    search_fields = ('title', 'anime_title_jp', 'studio', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'rating')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'status', 'author')
        }),
        ('Anime Details', {
            'fields': ('anime_title_jp', 'anime_type', 'rating', 'episode_count', 'release_year', 'studio'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('featured_image', 'thumbnail'),
            'classes': ('collapse',)
        }),
        ('Classification', {
            'fields': ('category', 'tags'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ('tags',)
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        if not obj.slug:
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'content')
    list_editable = ('is_approved',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    list_editable = ('is_active',)
    date_hierarchy = 'subscribed_at'
    ordering = ('-subscribed_at',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject', 'is_read', 'created_at')
        }),
        ('Message', {
            'fields': ('message',)
        }),
    )

# Customize admin site
admin.site.site_header = 'AnimeVerse Admin'
admin.site.site_title = 'AnimeVerse Admin'
admin.site.index_title = 'Welcome to AnimeVerse Administration'