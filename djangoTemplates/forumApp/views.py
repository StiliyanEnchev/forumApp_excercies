from datetime import datetime

from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from djangoTemplates.forumApp.forms import PostCreateForm, PostDeleteForm, SearchForm, PostEditForm
from djangoTemplates.forumApp.models import Post


# Create your views here.


def index(request):
    post_form = modelform_factory(
        Post,
        fields=('title', 'content', 'author', 'languages'),
    )

    context = {
        'my_form': post_form,
    }

    return render(request, "common/index.html", context)


class IndexView(TemplateView):
    template_name = 'common/index.html'
    extra_context = {
        'static_time': datetime.now(),
    }

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['dashboard.html']
        else:
            return ['common/index.html']


def dashboard(request):
    form = SearchForm(request.GET)
    posts = Post.objects.all()

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
    post = Post.objects.get(pk=pk)


    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = PostEditForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'posts/edit-template.html', context)

def details_page(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        pass

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