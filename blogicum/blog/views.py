from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Category, Comment
from .forms import ProfileForm, PostForm, CommentForm

POSTS_PER_PAGE = 10

User = get_user_model()


def get_actual_posts():
    return Post.objects.filter(
        is_published=True, category__is_published=True,
        pub_date__lt=timezone.now())


def index(request):
    posts = get_actual_posts()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, pk):
    post = get_object_or_404(get_actual_posts().filter(pk=pk))
    form = CommentForm()
    context = {}
    context['form'] = form
    context['post'] = post
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    posts = get_actual_posts().filter(category=category)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html',
                  {'category': category_slug, 'page_obj': page_obj})


@login_required
def create_post(request, pk=None):
    if pk:
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            url = reverse('blog:post_detail', args=[post.id])
            return redirect(url)
    else:
        post = None
    context = {}
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    context['form'] = form
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:post_detail', pk=pk)
    return render(request, 'blog/create.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user.username != username:
        posts = get_actual_posts().filter(author__username=username)
    else:
        posts = Post.objects.filter(author__username=username)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/profile.html', {
        'profile': user,
        'page_obj': page_obj})


def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.POST:
        if form.is_valid():
            form.save()
        url = reverse('blog:profile', args=[request.user.username])
        return redirect(url)
    else:
        return render(request, 'blog/user.html', {'form': form})


def add_comment(request, pk):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = get_object_or_404(Post, pk=pk)
        comment.save()
    return redirect('blog:post_detail', pk=pk)


def delete_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.POST:
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return redirect('blog:post_detail', pk=pk)
    return render(request, 'blog/comment.html', {'comment': comment})


def edit_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    form = CommentForm(request.POST or None, instance=comment)
    if request.POST:
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            form.save()
        return redirect('blog:post_detail', pk=pk)
    context = {}
    context['form'] = form
    context['comment'] = comment
    return render(request, 'blog/comment.html', context)


def delete_post(request, pk=None):
    post = get_object_or_404(get_actual_posts().filter(pk=pk))
    form = PostForm(request.POST or None, instance=post)
    context = {}
    context['form'] = form
    context['post'] = post
    return render(request, 'blog/detail.html', context)
