from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreateModel, PublishedModel

User = get_user_model()


class Post(PublishedModel, CreateModel):
    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата и время публикации',
                                    help_text='Если установить дату и время в '
                                    'будущем — можно делать отложенные '
                                    'публикации.')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор публикации')
    location = models.ForeignKey('Location', on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True, verbose_name='Местоположение')
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True,
        verbose_name='Категория')
    image = models.ImageField(
        'Изображение', blank=True, upload_to='post_images')

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.count()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['pub_date']


class Category(PublishedModel, CreateModel):
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField('Идентификатор', unique=True,
                            help_text='Идентификатор страницы для URL; '
                            'разрешены символы латиницы, цифры, дефис и '
                            'подчёркивание.')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(PublishedModel, CreateModel):
    name = models.CharField('Название места', max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Comment(CreateModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    text = models.TextField('Комментарий', blank=False)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
