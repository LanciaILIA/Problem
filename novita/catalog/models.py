from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.forms import UserCreationForm
from django import forms


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

class User(models.Model):
    name = models.CharField(max_length=20)
 
class Account(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)

notizia = 'NT'
articolo = 'AR'

POSITIONS = [
    (notizia, 'Новость'),
    (articolo, 'Статья')
]


class Author(models.Model): # Автор
   
    rating = models.IntegerField(verbose_name = "Рейтинг пользователя",
                                 default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    
    def update_rating(self):
        post_rating = self.post_set.aggregate(pr=Coalesce(Sum('rating'), 0)).get('pr')
        comment_rating = self.post_set.aggregate(cr=Coalesce(Sum('rating'), 0)).get('cr')
        self.rating = post_rating * 3 + comment_rating
        self.save()

    def __str__(self):
        return self.user.name


class Category(models.Model): # Категория
    name = models.CharField(max_length = 100,
                            help_text = "Введите категорию",
                            unique = True,
                            verbose_name = "Категория")

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE,
                               help_text="Выберите автора новости/статьи",
                               verbose_name="Автор новости/статьи",
                               null=True)
    category = models.ManyToManyField('Category', through = 'PostCategory',
                                    help_text = "Выберите категорию",
                                    verbose_name = "Категория")
    rating = models.IntegerField(verbose_name = "Рейтинг статьи",
                                 default=0)
    name = models.CharField(max_length = 100,
                            help_text = "Введите заголовок статьи / новости",
                            verbose_name = "Заголовок статьи / новости")
    title = models.TextField(max_length = 1000,
                             help_text = "Текст статьи / новости",
                             verbose_name = "Текст статьи / новости",
                             blank=True)
    data = models.DateTimeField(auto_now_add = True)
    position = models.CharField(max_length = 2,
                            choices = POSITIONS,
                            default = notizia)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.name

    def preview(self):
        small_title = self.title[0:124] + '...'
        return small_title

    def get_absolute_url (self):
        return reverse('news-detail', args=[str(self.id)])


class PostCategory(models.Model): # Промежуточная таблица
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)


class Comment(models.Model): # Комментарий
    title = models.TextField(max_length = 1000,
                             help_text = "Текст комментария",
                             verbose_name = "Комментарий",
                             blank=True)
    data = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(verbose_name = "Рейтинг комментария",
                                 default=0)
    post = models.ForeignKey('Post', on_delete=models.CASCADE,
                             help_text="Выберите новость/статью для комментария",
                             verbose_name="Выбор новости/статьи",
                             null=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.title




