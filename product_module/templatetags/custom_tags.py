from django import template
from product_module.models import Comment


register = template.Library()

@register.simple_tag
def get_comment_by_id(comment_id):
    comment_id = int(comment_id)
    try:
        comment = Comment.objects.get(pk=comment_id)
        author = comment.author.get_username()
        return author
    except:
        return ""
