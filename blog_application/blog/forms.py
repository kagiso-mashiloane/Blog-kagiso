from django import forms

from .models import Post, Category, Comment

from django.contrib.auth.forms import UserCreationForm  # Ensure this import is present
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('Article_Title', 'Article_Text', 'image')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['Article_Title', 'Article_Text','image', 'Article_Category' ]

    # Optionally, you can customize the widget or fields to adjust the UI
    Article_Category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")



class CustomUserCreationForm(UserCreationForm):
    # Add first name and last name fields
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    
    # Optional: You can include more custom fields, such as email validation
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')    

#comment section

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']        