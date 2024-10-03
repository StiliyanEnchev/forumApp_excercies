from django.db import models
from djangoTemplates.forumApp.Choices import LanguageChoice


# Create your models here.




class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    languages = models.CharField(choices=LanguageChoice.choices,
                                 default=LanguageChoice.OTHER,
                                 max_length=20)