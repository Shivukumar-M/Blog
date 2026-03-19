from mongoengine import Document, StringField, IntField, FloatField, \
    DateTimeField, BooleanField, ListField, ReferenceField, EmailField
from django.urls import reverse
from django.utils.text import slugify
from datetime import datetime


class Category(Document):
    name = StringField(max_length=100, required=True, unique=True)
    slug = StringField(unique=True, required=True)
    description = StringField()
    color = StringField(max_length=7, default='#6366f1')  # Hex color for category
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'categories',
        'indexes': ['slug', 'name'],
        'ordering': ['name']
    }
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('category_posts', kwargs={'slug': self.slug})
    
    def get_post_count(self):
        """Get number of published posts in this category"""
        return Post.objects(category=self, status='published').count()


class Tag(Document):
    name = StringField(max_length=50, required=True, unique=True)
    slug = StringField(unique=True, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'tags',
        'indexes': ['slug', 'name'],
        'ordering': ['name']
    }
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('tag_posts', kwargs={'slug': self.slug})
    
    def get_post_count(self):
        """Get number of published posts with this tag"""
        return Post.objects(tags=self, status='published').count()


class Post(Document):
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
    
    title = StringField(max_length=255, required=True)
    slug = StringField(unique=True, required=True)
    content = StringField(required=True)
    excerpt = StringField(max_length=300)
    
    # Anime-specific fields
    anime_title_jp = StringField(max_length=255)
    anime_type = StringField(max_length=10, choices=ANIME_TYPES)
    rating = FloatField(min_value=0, max_value=10)
    episode_count = IntField()
    release_year = IntField()
    studio = StringField(max_length=100)
    
    # Images (URLs/paths for Cloudinary)
    featured_image = StringField()
    thumbnail = StringField()
    
    # Metadata
    author_id = IntField(required=True)  # Django User ID
    author_username = StringField(required=True)  # Store username for reference
    category = ReferenceField(Category, null=True)
    tags = ListField(ReferenceField(Tag))
    status = StringField(max_length=10, choices=STATUS_CHOICES, default='published')
    
    # SEO fields
    meta_description = StringField(max_length=160)
    meta_keywords = StringField(max_length=255)
    
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    views = IntField(default=0)
    
    meta = {
        'collection': 'posts',
        'indexes': ['slug', 'status', 'author_id', 'created_at', '-created_at'],
        'ordering': ['-created_at']
    }
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
            
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while Post.objects(slug=self.slug, id__ne=self.id).first():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save()
    
    @property
    def is_featured(self):
        """Check if post should be featured (high rating)"""
        return self.rating and self.rating >= 8.0
    
    @property
    def reading_time(self):
        """Calculate estimated reading time"""
        word_count = len(self.content.split())
        return max(1, word_count // 200)  # Assuming 200 words per minute
    
    def get_comments(self):
        """Get approved comments for this post"""
        return Comment.objects(post=self, is_approved=True).order_by('-created_at')


class Comment(Document):
    post = ReferenceField(Post, required=True)
    name = StringField(max_length=255, required=True)
    email = EmailField(required=True)
    content = StringField(required=True)
    is_approved = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'comments',
        'indexes': ['post', 'created_at', '-created_at'],
        'ordering': ['-created_at']
    }
    
    def __str__(self):
        return f'{self.name} - {self.post.title[:50]}'


class Newsletter(Document):
    email = EmailField(required=True, unique=True)
    subscribed_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    
    meta = {
        'collection': 'newsletter_subscribers',
        'indexes': ['email', '-subscribed_at'],
        'ordering': ['-subscribed_at']
    }
    
    def __str__(self):
        return self.email


class Contact(Document):
    name = StringField(max_length=100, required=True)
    email = EmailField(required=True)
    subject = StringField(max_length=200, required=True)
    message = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    is_read = BooleanField(default=False)
    
    meta = {
        'collection': 'contact_messages',
        'indexes': ['email', 'created_at', '-created_at'],
        'ordering': ['-created_at']
    }
    
    def __str__(self):
        return f'{self.name} - {self.subject[:30]}'