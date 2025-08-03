from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
import os

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6366f1')  # Hex color for category
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_posts', kwargs={'slug': self.slug})

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('tag_posts', kwargs={'slug': self.slug})

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    ANIME_TYPES = [
        ('tv', 'TV Series'),
        ('movie', 'Movie'),
        ('ova', 'OVA'),
        ('special', 'Special'),
        ('ona', 'ONA'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, help_text="Brief description for preview")
    
    # Anime-specific fields
    anime_title_jp = models.CharField(max_length=255, blank=True, help_text="Japanese title", verbose_name="Japanese Title")
    anime_type = models.CharField(max_length=10, choices=ANIME_TYPES, blank=True, verbose_name="Anime Type")
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, help_text="Rating out of 10")
    episode_count = models.IntegerField(null=True, blank=True, verbose_name="Episode Count")
    release_year = models.IntegerField(null=True, blank=True, verbose_name="Release Year")
    studio = models.CharField(max_length=100, blank=True)
    
    # Images
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Featured Image")
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    
    # Metadata
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    
    # SEO fields
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta Description")
    meta_keywords = models.CharField(max_length=255, blank=True, verbose_name="Meta Keywords")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
            
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)
        
        # Optimize images after saving
        if self.featured_image:
            self.optimize_image(self.featured_image.path, max_size=(1200, 600))
        if self.thumbnail:
            self.optimize_image(self.thumbnail.path, max_size=(400, 300))
    
    def optimize_image(self, image_path, max_size):
        """Optimize uploaded images"""
        try:
            if os.path.exists(image_path):
                with Image.open(image_path) as img:
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Resize if larger than max_size
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Save optimized image
                    img.save(image_path, optimize=True, quality=85)
        except Exception as e:
            print(f"Error optimizing image {image_path}: {e}")
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    @property
    def is_featured(self):
        """Check if post should be featured (high rating)"""
        return self.rating and self.rating >= 8.0
    
    @property
    def reading_time(self):
        """Calculate estimated reading time"""
        word_count = len(self.content.split())
        return max(1, word_count // 200)  # Assuming 200 words per minute

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return f'{self.name} - {self.post.title[:50]}'

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        
    def __str__(self):
        return self.email

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.name} - {self.subject[:30]}'