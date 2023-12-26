# D6
from django.urls import path
from .views import NewsListView, NewsDetailView, PostUpdate, CategoryListView, CategoryDetailView, subscrlbe

urlpatterns = [
    path('', NewsListView.as_view(), name='news-list'),
    path('<int:pk>', NewsDetailView.as_view(), name='news-detail'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='news-update'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'), # D9 ссылка на стр с категориями
    path('category/<int:pk>/subscrlbe', subscrlbe, name='subscrlbe'),
]