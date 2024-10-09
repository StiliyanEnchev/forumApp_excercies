from django import forms
from django.core.exceptions import ValidationError

from djangoTemplates.forumApp.Choices import LanguageChoice
from djangoTemplates.forumApp.mixins import DisableFieldsMixin
from djangoTemplates.forumApp.models import Post


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

        error_messages = {
            'title': {
                'required': 'please enter the title as it is requred',
                'max_length': 'title is too long',
            },
            'author': {
                'required': 'please enter an author'
            }
        }


    def clean_author(self):     # check if the author starts with upper case and raise ValError if not
        author = self.cleaned_data['author']

        if author[0] != author[0].upper():
            raise ValidationError('The author must start with upper case')

        return author

    def clean(self):            # if title is in contect it raise ValError else returns the clenaed data
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and content and title in content:
            raise ValidationError('The title cannot be in content')

        return cleaned_data


class PostCreateForm(PostBaseForm):
    pass


class PostEditForm(PostBaseForm):
    pass


class PostDeleteForm(PostBaseForm, DisableFieldsMixin):
    pass


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        error_messages={
            'required': 'please write something',
            'max_length': 'max length is ten'
        },
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for a post'
            }
        )
    )