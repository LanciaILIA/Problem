# D6
from django.urls import path
from .views import NewsListView, NewsDetailView, PostUpdate

urlpatterns = [
    path('', NewsListView.as_view(), name='news-list'),
    path('<int:pk>', NewsDetailView.as_view(), name='news-detail'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='news-update'),
]