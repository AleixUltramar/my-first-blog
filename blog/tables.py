import django_tables2 as tables
from django.utils.html import format_html
from django_tables2 import columns
from django_tables2.utils import A

from .models import Post


class PublishedDateColumn(tables.DateTimeColumn):
    def render(self, value, *args, **kwargs):
        val = super().render(value=value, *args, **kwargs)
        return format_html('<div class="date">{}</div>', val)  # o template_name..


class PersonTable(tables.Table):
    title = columns.LinkColumn("post_detail", args=[A("pk")])
    published_date = PublishedDateColumn()
    options = tables.TemplateColumn(template_name="blog/option_list.html")

    class Meta:
        model = Post
        sequence = (
            "title",
            "text",
            "author",
            "published_date",
            "options",
        )
        exclude = ("id", "created_date")

    def render_text(self, value):
        return value or "linebreaksbr"
