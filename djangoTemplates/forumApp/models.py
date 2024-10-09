from django.db import models
from djangoTemplates.forumApp.Choices import LanguageChoice


# Create your models here.




class Post(models.Model):
    TITLE_MAX_LENGTH = 100

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    content = models.TextField()
    author = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    languages = models.CharField(choices=LanguageChoice.choices,
                                 default=LanguageChoice.OTHER,
                                 max_length=20)
