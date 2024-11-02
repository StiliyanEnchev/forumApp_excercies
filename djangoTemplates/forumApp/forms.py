
from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from djangoTemplates.forumApp.Choices import LanguageChoice
from djangoTemplates.forumApp.mixins import DisableFieldsMixin
from djangoTemplates.forumApp.models import Post, Comment


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['approved']

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

    def clean(self):            # if title is in content it raise ValError else returns the cleaned data
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and content and title in content:
            raise ValidationError('The title cannot be in content')

        return cleaned_data


    def save(self, commit=True): #overrites the save to save the post title capitalized in the DB
        post = super().save(commit=False)

        post.title = post.title.capitalize()

        if commit:
            post.save()

        return post

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'content')
        labels = {
            "author": '',
            'content': '',
        }

        error_messages = {
            'author': {
                'required': 'please enter an author'
            },
            'content': {
                'required': 'please write something',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['author'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your name',
        })

        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Add message...',
        })


CommentFormSet = formset_factory(CommentForm, extra=3)