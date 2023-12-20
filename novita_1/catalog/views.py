from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import *
from django.views import generic
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView


def index(request): # Получение данных из БД
    num_post = Post.objects.all().count() # objects.all() - Получить все объекты Book из БД
    num_comment = Comment.objects.all().count()
    num_category = Category.objects.all().count()
    num_authors = Author.objects.count() # count() => SELECT COUNT(*)

    return render(request,'index.html',  # render - Формирует и возвращает ответ (НТМL-страницу index.html)
                    context={'num_post' : num_post,
                            'num_comment' : num_comment,
                             'num_category' : num_category,
                             'num_authors' : num_authors,
                            }
                   )
    # 'num_visits' : num_visits,
    # return HttpResponse("Глaвнaя страница сайта Мир книг!")

class NewsListView(generic.ListView): # D6
    model = Post
    ordering = 'name'
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

    def get_queryset_(self): # сортировка по дате
        queryset = Post.objects.all().order_by('-data')
        return queryset


class NewsDetailView(generic.DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'news_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news_detail'

def news_add(request):
    post = Post.objects.all()
    postform = PostForm()
    return render(request, "news_add.html",
                  {"form": postform, "post": post})

def create(request):
    if request.method == "POST":
        post = Post()
        post.name = request.POST.get("name")
        post.title = request.POST.get("title")
        post.save()
        return HttpResponseRedirect("/news_add/")

def delete(request, id):
    try:
       name = Post.objects.get(id=id)
       name.delete()
       return HttpResponseRedirect("/news_add/")
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Статья не найдена</h2>")

def editl(request, id):
    name = Post.objects.get(id=id)
    if request.method == "POST":
        name.name = request.POST.get("name")
        name.save()
        return HttpResponseRedirect("/news_add/")
    else:
        return render(request, "editl.html", {"name": name})

class PostUpdate(generic.UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'editl.html'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = 'person/'