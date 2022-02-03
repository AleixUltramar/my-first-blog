from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

from .models import Post
from .forms import PostForm
from .tables import PersonTable

class ListPostView(ExportMixin, SingleTableView): # equals: (SingleTableMixin, generic.ListView)
    template_name = "blog/post_list.html"
    table_class = PersonTable
    context_object_name = "posts"
    table_pagination = {
        "per_page": 4
    }
    export_formats = ['csv', 'json', 'ods', 'xls']

    def get_queryset(self):
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
            "published_date"
        )
        return posts


class DetailPostView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class CreatePostView(generic.CreateView):
    template_name = "blog/post_edit.html"
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.published_date = timezone.now()
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})


class EditPostView(generic.UpdateView):
    template_name = "blog/post_edit.html"
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.published_date = timezone.now()
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})


class RemovePostView(generic.DeleteView):
    model = Post
    form = PostForm

    def get_success_url(self):
        return reverse("post_list")
