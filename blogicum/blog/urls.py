from django.urls import path, include
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('create_post', views.create_post, name='create_post'),
    path('profile/<slug:username>', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]

