from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    text = forms.CharField(max_length=200)

    class Meta:
        model = Comment
        fields = ['text']
