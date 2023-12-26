from django import forms
from catalog.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'name', 'category']

        labels = {
            'title': 'Содержание',
            'name': 'Заголовок',
            'category': 'Категория'
        }

        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-text', 'cols': 80, 'rows': 15}),
        }
