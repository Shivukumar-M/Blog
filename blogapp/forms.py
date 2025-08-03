from django import forms
from .models import Comment, Newsletter, Contact, Post, Category, Tag

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        
        # Common styling for text inputs
        text_input_classes = 'w-full py-3 px-4 bg-white/5 border border-white/20 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-300 text-white placeholder-gray-400'
        
        # Common styling for select inputs
        select_classes = 'w-full py-3 px-4 bg-white/5 border border-white/20 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-300 text-white'
        
        # Common styling for textarea
        textarea_classes = 'w-full py-3 px-4 bg-white/5 border border-white/20 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-300 text-white placeholder-gray-400 resize-vertical'
        
        # File input styling
        file_classes = 'w-full py-3 px-4 bg-white/5 border border-white/20 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary/50 transition-all duration-300 text-white file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:bg-primary/80'
        
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

    class Meta:
        model = Post
        fields = [
            'title', 'excerpt', 'content', 'anime_title_jp', 'anime_type', 
            'rating', 'episode_count', 'release_year', 'studio', 'category', 
            'tags', 'featured_image', 'thumbnail', 'meta_description', 'meta_keywords'
        ]
        
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

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'w-full py-3 px-4 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Your Name'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'w-full py-3 px-4 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'your.email@example.com'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'w-full py-3 px-4 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 resize-none',
            'placeholder': 'Share your thoughts about this anime...',
            'rows': 4
        })

    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
        
    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters long.")
        return content

class NewsletterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'w-full py-3 px-4 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Enter your email for anime updates...'
        })

    class Meta:
        model = Newsletter
        fields = ('email',)

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        
        # Common styling for all fields
        common_classes = 'w-full py-3 px-4 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200'
        
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

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
        
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message

class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full py-2 px-4 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Search for anime reviews, characters, studios...'
        })
    )