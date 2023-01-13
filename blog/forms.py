from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            'username': 'Your name',
            'user_email': 'Your email address',
            'text': 'Your comment'
        }
