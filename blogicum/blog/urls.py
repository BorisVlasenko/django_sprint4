from django.urls import path, include
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('create_post', views.create_post, name='create_post'),
    path('posts/<int:pk>/edit', views.create_post, name='edit_post'),
    path('profile/<slug:username>', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('post/<int:pk>/comment', views.add_comment, name='add_comment'),

    path('post/<int:pk>/edit_comment/<int:comment_pk>',
         views.edit_comment, name='edit_comment'),

    path('post/<int:pk>/delete_comment/<int:comment_pk>',
         views.delete_comment, name='delete_comment'),

    path('post/<int:pk>/delete', views.delete_post, name='delete_post'),

]
