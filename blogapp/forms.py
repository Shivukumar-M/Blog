from django import forms
from .models import Comment, Newsletter, Contact

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