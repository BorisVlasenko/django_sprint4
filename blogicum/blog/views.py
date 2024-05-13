from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment
from .forms import ProfileForm, PostForm, CommentForm
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .utils import get_actual_posts, get_page_obj

User = get_user_model()


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        success_url = reverse_lazy('blog:post_detail', kwargs={'pk': pk})
        return success_url

    def get_object(self, queryset=None):
        comment_pk = self.kwargs.get('comment_pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.author == self.request.user:
            return comment
        else:
            raise PermissionDenied


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        success_url = reverse_lazy('blog:profile',
                                   kwargs={'username':
                                           self.request.user.username})
        return success_url

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        if post.author == self.request.user:
            return post
        else:
            raise PermissionDenied


def index(request):
    posts = get_actual_posts()
    page_number = request.GET.get('page')
    page_obj = get_page_obj(posts, page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.is_published or post.author == request.user:
        form = CommentForm()
        context = {}
        context['form'] = form
        context['post'] = post
    else:
        raise Http404()
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    posts = get_actual_posts().filter(category=category)
    page_number = request.GET.get('page')
    page_obj = get_page_obj(posts, page_number)
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
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        posts = get_actual_posts().filter(author__username=username)
    else:
        posts = (Post.objects
                 .filter(author__username=username)
                 .order_by('-pub_date'))

    page_number = request.GET.get('page')
    page_obj = get_page_obj(posts, page_number)
    return render(request, 'blog/profile.html', {
        'profile': user,
        'page_obj': page_obj})


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        url = reverse('blog:profile', args=[request.user.username])
        return redirect(url)
    else:
        return render(request, 'blog/user.html', {'form': form})


@login_required
def add_comment(request, pk):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = get_object_or_404(Post, pk=pk)
        comment.save()
    return redirect('blog:post_detail', pk=pk)


@login_required
def edit_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.author == request.user or request.user.is_superuser:
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=pk)
        context = {}
        context['form'] = form
        context['comment'] = comment
        return render(request, 'blog/comment.html', context)
    raise PermissionDenied
