from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from .models import Post, Category
from django.utils import timezone
from .forms import ProfileForm
from django.contrib.auth import get_user_model

POSTS_PER_PAGE = 5

User = get_user_model()


def get_actual_posts():
    return Post.objects.filter(
        is_published=True, category__is_published=True,
        pub_date__lt=timezone.now())


def index(request):
    posts = get_actual_posts()[:POSTS_PER_PAGE]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, id):
    post = get_object_or_404(get_actual_posts().filter(id=id))
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    posts = get_actual_posts().filter(category=category)
    return render(request, 'blog/category.html',
                  {'category': category_slug, 'post_list': posts})


def create_post(request):
    return HttpResponse('create_post')


def profile(request, username):
    return render(request, 'blog/profile.html', {'profile': request.user})


def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.POST:
        form.save()
        url = reverse('blog:profile', args=[request.user.username])
        return redirect(url)
    else:
        return render(request, 'blog/user.html', {'form': form})
        
