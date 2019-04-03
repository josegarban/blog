from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'status')


class EmailPostForm(forms.Form):
    name     = forms.CharField (max_length=30)
    email    = forms.EmailField()
    to       = forms.EmailField()
    comments = forms.CharField (required=False,
                                widget=forms.Textarea)
