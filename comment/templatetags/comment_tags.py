from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment

register = template.Library()


@register.simple_tag
def comments_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()