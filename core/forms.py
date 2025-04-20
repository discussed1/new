from django import forms
from django.contrib.auth.models import User
from .models import Profile, Community, Post, Comment, Payment

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'display_name', 'country', 'website', 'interests', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell the community about yourself', 'rows': 3}),
            'display_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your display name (optional)'}),
            'country': forms.Select(attrs={'class': 'form-control form-select'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Your website (optional)'}),
            'interests': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your interests separated by commas'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Community name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Community description', 'rows': 4}),
        }

class TextPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Post content', 'rows': 6}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags (comma separated)'}),
        }
    
class LinkPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'url', 'tags']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags (comma separated)'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a comment...', 'rows': 2}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search...'}),
    )

class DonationForm(forms.ModelForm):
    custom_amount = forms.DecimalField(
        required=False,
        min_value=1,
        max_value=1000,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Custom amount (USD)',
            'step': '0.01',
            'min': '1',
            'max': '1000'
        })
    )
    
    class Meta:
        model = Payment
        fields = ['donation_type', 'description']
        widgets = {
            'donation_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Reason for donation (optional)',
                'rows': 3
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        donation_type = cleaned_data.get('donation_type')
        custom_amount = cleaned_data.get('custom_amount')
        
        # Validate that if donation_type is Custom (0), then custom_amount is required
        if donation_type == 0 and not custom_amount:
            self.add_error('custom_amount', 'Please enter a custom amount')
        
        # Set the amount field based on donation type to ensure it's never null
        if donation_type == 0 and custom_amount:
            # For custom amount
            cleaned_data['amount'] = custom_amount
        elif donation_type == 5:
            # Small donation
            cleaned_data['amount'] = 5
        elif donation_type == 10:
            # Medium donation
            cleaned_data['amount'] = 10
        elif donation_type == 25:
            # Large donation
            cleaned_data['amount'] = 25
        else:
            # Default fallback
            cleaned_data['amount'] = 5
        
        return cleaned_data
