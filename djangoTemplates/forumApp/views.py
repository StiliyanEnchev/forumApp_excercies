from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, RedirectView, ListView, FormView, CreateView, UpdateView, DeleteView, \
    DetailView

from djangoTemplates.forumApp.decorators import measure_execution_time
from djangoTemplates.forumApp.forms import PostCreateForm, PostDeleteForm, SearchForm, PostEditForm, CommentFormSet
from djangoTemplates.forumApp.mixins import TimeRestrictedMixin
from djangoTemplates.forumApp.models import Post


# Create your views here.

class RedirectHomeView(RedirectView):
    url = reverse_lazy('dashboard')


@method_decorator(measure_execution_time, name='dispatch')
class IndexView(TimeRestrictedMixin, TemplateView):
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


class DashboardListView(ListView, FormView):
    template_name = 'dashboard.html'
    context_object_name = 'posts'
    form_class = SearchForm
    success_url = reverse_lazy('dashboard')
    model = Post
    paginate_by = 2

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


class DetailsView(DetailView):
    model = Post
    template_name = 'posts/details-post.html'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        formset = CommentFormSet(request.POST)

        if formset.is_valid:
            for form in formset:
                if form.cleaned_data:
                    comment = form.save(commit=False)
                    comment.post = post
                    comment.save()

            return redirect('details-post', pk=post.id)

        context = self.get_context_data()
        context['formset'] = formset

        return self.render_to_response(context)

class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/add-post.html'
    success_url = reverse_lazy('dashboard')


class DeletePostView(DeleteView):
    model = Post
    template_name = 'posts/delete-template.html'
    success_url = reverse_lazy('dashboard')
