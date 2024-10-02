from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

from djangoTemplates.forumApp.forms import PostBaseForm
from djangoTemplates.forumApp.models import Post


# Create your views here.

def index(request):

    context = {
        'posts': '',
    }

    return render(request, "base.html", context)

def dashboard(request):
    context = {
        "posts": Post.objects.all(),
    }

    return render(request, 'dashboard.html', context)


def add_post(request):

    form = PostBaseForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        'form': form,
    }

    return render(request, 'posts/add-post.html', context)
