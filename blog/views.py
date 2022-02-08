from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic.base import ContextMixin
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

from .models import Post
from .forms import PostForm
from .tables import PersonTable


class TemplateMixin(ContextMixin):
    def get_template_base(self):
        num_template = (self.request.user.id % 5) + 1 if self.request.user.id else ""
        template = "blog/base%s.html" % (num_template,)
        return template

    def get_context_data(self, **kwargs):
        # para añadir el "template_base" como variable en los templates (en vez de usar directamente el método
        # "get_template_base" desde los templates)
        kwargs['template_base'] = self.get_template_base()
        return super().get_context_data(**kwargs)


class ListPostView(
    TemplateMixin, ExportMixin, SingleTableView
):
    template_name = "blog/post_list.html"
    table_class = PersonTable
    context_object_name = "posts"
    table_pagination = {"per_page": 10}
    export_formats = ["csv", "json", "ods", "xls"]

    def get_queryset(self):
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
            "published_date"
        )
        return posts


class DetailPostView(TemplateMixin, generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class CreatePostView(LoginRequiredMixin, TemplateMixin, generic.CreateView):
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


class EditPostView(LoginRequiredMixin, TemplateMixin, generic.UpdateView):
    template_name = "blog/post_edit.html"
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        # post.author = self.request.user # ya no hace falta modificarlo, porque tiene que ser el mismo autor
        post.published_date = timezone.now()
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})

    def dispatch(self, request, *args, **kwargs):  # Lo mejor sería hacer la validación en el método "get_object" en vez del dispatch!
        if self.get_object().author != self.request.user:
            messages.error(self.request, "You are not allowed to edit this entry!")
            return HttpResponseRedirect(reverse("post_list"))
        return super().dispatch(request, *args, **kwargs)


class RemovePostView(LoginRequiredMixin, TemplateMixin, generic.DeleteView):
    model = Post
    form = PostForm

    def get_success_url(self):
        return reverse("post_list")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            messages.error(self.request, "You are not allowed to delete this entry!")
            return HttpResponseRedirect(reverse("post_list"))
        return super().dispatch(request, *args, **kwargs)
