from .models import Post
from django.utils import timezone
from django.core.paginator import Paginator

POSTS_PER_PAGE = 10


def get_actual_posts():
    return Post.objects.filter(
        is_published=True, category__is_published=True,
        pub_date__lt=timezone.now()).order_by('-pub_date')


def get_page_obj(posts, page_number):
    paginator = Paginator(posts, POSTS_PER_PAGE)
    return paginator.get_page(page_number)
