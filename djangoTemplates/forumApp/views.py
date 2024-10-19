from datetime import datetime

from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView, ListView, FormView, CreateView, UpdateView, DeleteView

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


class RedirectHomeView(RedirectView):
    url = reverse_lazy('dashboard')


class IndexView(TemplateView):
    template_name = 'common/index.html'
    extra_context = {
        'static_time': datetime.now(),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['dynamic_time'] = datetime.now()

        return context


    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['dashboard.html']
        else:
            return ['common/index.html']


# def dashboard(request):
#     form = SearchForm(request.GET)
#     posts = Post.objects.all()
#
#     if request.method == "GET":
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             posts = posts.filter(title__icontains=query)
#
#     context = {
#         "posts": posts,
#         'form': form,
#     }
#
#     return render(request, 'dashboard.html', context)


class DashboardListView(ListView, FormView):
    template_name = 'dashboard.html'
    context_object_name = 'posts'
    form_class = SearchForm
    success_url = reverse_lazy('dashboard')
    model = Post

    def get_queryset(self):
        queryset = self.model.objects.all()

        if 'query' in self.request.GET:
            query = self.request.GET.get('query')
            queryset = queryset.filter(title__icontains=query)

        return queryset


class EditPostView(UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'posts/edit-template.html'
    success_url = reverse_lazy('dashboard')

# def edit_post(request, pk):
#     post = Post.objects.get(pk=pk)
#
#
#     if request.method == 'POST':
#         form = PostEditForm(request.POST, instance=post)
#
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#
#     else:
#         form = PostEditForm(instance=post)
#
#     context = {
#         'form': form,
#         'post': post,
#     }
#
#     return render(request, 'posts/edit-template.html', context)

def details_page(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        pass

    context = {
        'post': post,
    }

    return render(request, 'posts/details-post.html', context)


class AddPostView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/add-post.html'
    success_url = reverse_lazy('dashboard')


# def add_post(request):
#
#     form = PostCreateForm(request.POST or None)
#
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'posts/add-post.html', context)


class DeletePostView(DeleteView):
    model = Post
    template_name = 'posts/delete-template.html'
    success_url = reverse_lazy('dashboard')

# def delete_post(request, pk: int):
#     post = Post.objects.get(pk=pk)
#     form = PostDeleteForm(instance=post)
#
#     if request.method == 'POST':
#         post.delete()
#         return redirect('dashboard')
#
#     context = {
#         'form': form,
#         'post': post,
#     }
#
#     return render(request, 'posts/delete-template.html', context)