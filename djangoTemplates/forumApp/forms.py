from django import forms

from djangoTemplates.forumApp.Choices import LanguageChoice
from djangoTemplates.forumApp.models import Post


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

        labels = {
            'title': 'here is the title'
        }