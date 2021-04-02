import django_filters
from django_filters import CharFilter

from api.models import Post


class PostFilter(django_filters.FilterSet):
    post_title = CharFilter(field_name='post_title', lookup_expr='icontains')
    post_text = CharFilter(field_name='post_text', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['post_title', 'tags', 'post_text']