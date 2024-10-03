from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

from djangoTemplates.forumApp.forms import PostCreateForm, PostDeleteForm, SearchForm
from djangoTemplates.forumApp.models import Post


# Create your views here.

def index(request):

    context = {
        'posts': '',
    }

    return render(request, "base.html", context)


def dashboard(request):
    posts = Post.objects.all()
    form = SearchForm(request.GET)

    if request.method == "GET":
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = posts.filter(title__icontains=query)

    context = {
        "posts": posts,
        'form': form,
    }

    return render(request, 'dashboard.html', context)


def edit_post(request, pk):
    return HttpResponse()

def details_page(request, pk):
    post = Post.objects.get(pk=pk)

    context = {
        'post': post,
    }

    return render(request, 'posts/details-post.html', context)


def add_post(request):

    form = PostCreateForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        'form': form,
    }

    return render(request, 'posts/add-post.html', context)


def delete_post(request, pk: int):
    post = Post.objects.get(pk=pk)
    form = PostDeleteForm(instance=post)

    if request.method == 'POST':
        post.delete()
        return redirect('dashboard')

    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'posts/delete-template.html', context)