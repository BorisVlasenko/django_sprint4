from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<str:category_slug>/', views.category_posts,
         name='category_posts'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/edit/', views.create_post, name='edit_post'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),

    path('posts/<int:pk>/edit_comment/<int:comment_pk>/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:pk>/delete_comment/<int:comment_pk>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),

    path('posts/<int:pk>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'),

]
