from django import forms
from .models import Comment, Newsletter, Contact, Post, Category, Tag
import cloudinary.uploader
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):

     class Meta:
        model = User
        fields =['username','password1', 'password2',]



class PostForm(forms.Form):
    title = forms.CharField(max_length=255)
    excerpt = forms.CharField(max_length=300, widget=forms.Textarea)
    content = forms.CharField(widget=forms.Textarea)
    anime_title_jp = forms.CharField(max_length=255, required=False)
    anime_type = forms.ChoiceField(choices=Post.ANIME_TYPES, required=False)
    rating = forms.DecimalField(max_digits=3, decimal_places=1, required=False)
    episode_count = forms.IntegerField(required=False)
    release_year = forms.IntegerField(required=False)
    studio = forms.CharField(max_length=100, required=False)
    category = forms.ChoiceField(required=False)
    tags = forms.MultipleChoiceField(required=False)
    featured_image = forms.ImageField(required=False)
    thumbnail = forms.ImageField(required=False)
    meta_description = forms.CharField(max_length=160, required=False)
    meta_keywords = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [('', '---------')] + [
            (str(category.id), category.name) for category in Category.objects().order_by('name')
        ]
        self.fields['tags'].choices = [
            (str(tag.id), tag.name) for tag in Tag.objects().order_by('name')
        ]
        
        # Common styling for text inputs
        text_input_classes = ' w-full py-3 px-4 bg-white/5 border border-white/20 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-300 text-white placeholder-gray-400'
        
        # Common styling for select inputs
        select_classes = 'themed-select w-full py-3 px-4 border border-white/20 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-300 text-white'
        
        # Common styling for textarea
        textarea_classes = ' w-full py-3 px-4 bg-white/5 border border-white/20 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-300 text-white placeholder-gray-400 resize-vertical'
        
        # File input styling
        file_classes = ' w-full py-3 px-4 bg-white/5 border border-white/20 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-300 text-white file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:bg-primary/80'
        
        # Apply styling to fields
        self.fields['title'].widget.attrs.update({
            'class': text_input_classes,
            'placeholder': 'Enter your anime review title...'
        })
        
        self.fields['excerpt'].widget.attrs.update({
            'class': textarea_classes,
            'placeholder': 'Write a brief description of your review...',
            'rows': 3,
            'maxlength': 300
        })
        
        self.fields['content'].widget.attrs.update({
            'class': textarea_classes,
            'placeholder': 'Write your detailed anime review here...',
            'rows': 15
        })
        
        self.fields['anime_title_jp'].widget.attrs.update({
            'class': text_input_classes,
            'placeholder': 'アニメのタイトル (Japanese title)'
        })
        
        self.fields['anime_type'].widget.attrs.update({
            'class': select_classes
        })
        
        self.fields['rating'].widget.attrs.update({
            'class': text_input_classes,
            'placeholder': '8.5',
            'step': '0.1',
            'min': '0',
            'max': '10'
        })
        
        self.fields['episode_count'].widget.attrs.update({
            'class': text_input_classes,
            'placeholder': '12'
        })
        
        self.fields['release_year'].widget.attrs.update({
            'class': text_input_classes,
            'placeholder': '2024'
        })
        
        self.fields['studio'].widget.attrs.update({
            'class': text_input_classes,
            'placeholder': 'Studio Name'
        })
        
        self.fields['category'].widget.attrs.update({
            'class': select_classes
        })
        
        self.fields['tags'].widget.attrs.update({
            'class': select_classes + ' h-32'
        })
        
        self.fields['featured_image'].widget.attrs.update({
            'class': file_classes,
            'accept': 'image/*'
        })
        
        self.fields['thumbnail'].widget.attrs.update({
            'class': file_classes,
            'accept': 'image/*'
        })
        
        self.fields['meta_description'].widget.attrs.update({
            'class': text_input_classes,
            'placeholder': 'Brief description for search engines...',
            'maxlength': 160
        })
        
        self.fields['meta_keywords'].widget.attrs.update({
            'class': text_input_classes,
            'placeholder': 'anime, review, action, shounen'
        })

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title
        
    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 100:
            raise forms.ValidationError("Content must be at least 100 characters long.")
        return content
        
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 0 or rating > 10):
            raise forms.ValidationError("Rating must be between 0 and 10.")
        return rating
        
    def clean_release_year(self):
        release_year = self.cleaned_data.get('release_year')
        if release_year is not None and (release_year < 1900 or release_year > 2030):
            raise forms.ValidationError("Please enter a valid release year.")
        return release_year

    def save(self, author, status='published'):
        data = self.cleaned_data
        category = None
        category_id = data.get('category')
        if category_id:
            category = Category.objects(id=category_id).first()

        tag_ids = data.get('tags', [])
        tags = list(Tag.objects(id__in=tag_ids)) if tag_ids else []

        post = Post(
            title=data['title'],
            excerpt=data['excerpt'],
            content=data['content'],
            anime_title_jp=data.get('anime_title_jp', ''),
            anime_type=data.get('anime_type') or '',
            rating=float(data['rating']) if data.get('rating') is not None else None,
            episode_count=data.get('episode_count'),
            release_year=data.get('release_year'),
            studio=data.get('studio', ''),
            category=category,
            tags=tags,
            meta_description=data.get('meta_description', ''),
            meta_keywords=data.get('meta_keywords', ''),
            author_id=author.id,
            author_username=author.username,
            status=status,
        )

        featured_image = self.files.get('featured_image')
        thumbnail = self.files.get('thumbnail')
        if featured_image:
            try:
                upload_result = cloudinary.uploader.upload(featured_image, folder='blog_images')
                post.featured_image = upload_result.get('secure_url', featured_image.name)
            except Exception:
                fs = FileSystemStorage()
                filename = fs.save(f'uploads/{featured_image.name}', featured_image)
                post.featured_image = fs.url(filename)
        if thumbnail:
            try:
                upload_result = cloudinary.uploader.upload(thumbnail, folder='thumbnails')
                post.thumbnail = upload_result.get('secure_url', thumbnail.name)
            except Exception:
                fs = FileSystemStorage()
                filename = fs.save(f'uploads/{thumbnail.name}', thumbnail)
                post.thumbnail = fs.url(filename)

        post.save()
        return post

class CommentForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'text-black w-full py-3 px-4 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Your Name'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'text-black w-full py-3 px-4 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'your.email@example.com'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'text-black w-full py-3 px-4 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 resize-none',
            'placeholder': 'Share your thoughts about this anime...',
            'rows': 4
        })

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters long.")
        return content

    def save(self, post):
        comment = Comment(
            post=post,
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            content=self.cleaned_data['content'],
        )
        comment.save()
        return comment

class NewsletterForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'w-full py-3 px-4 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Enter your email for anime updates...'
        })

    def save(self):
        email = self.cleaned_data['email']
        newsletter = Newsletter.objects(email=email).first()
        created = False
        if not newsletter:
            newsletter = Newsletter(email=email)
            newsletter.save()
            created = True
        return newsletter, created

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        
        # Common styling for all fields
        common_classes = 'text-black w-full py-3 px-4 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200'
        
        self.fields['name'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Your Name'
        })
        self.fields['email'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'your.email@example.com'
        })
        self.fields['subject'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Subject of your message'
        })
        self.fields['message'].widget.attrs.update({
            'class': common_classes + ' resize-none',
            'placeholder': 'Tell us what\'s on your mind...',
            'rows': 6
        })

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message

    def save(self):
        contact = Contact(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            subject=self.cleaned_data['subject'],
            message=self.cleaned_data['message'],
        )
        contact.save()
        return contact

class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full py-2 px-4 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Search for anime reviews, characters, studios...'
        })
    )