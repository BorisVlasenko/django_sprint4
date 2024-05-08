from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Comment


User = get_user_model()


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'last_name', 'email',)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('is_published',
                  'title',
                  'image',
                  'pub_date',
                  'text',
                  'location',
                  'category',
                  )
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('id', 'text',)
