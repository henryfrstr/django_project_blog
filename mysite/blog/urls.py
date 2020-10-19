from django.urls import path
from .views import home_view, post_detail_view, CategoryListView, post_search

app_name = 'blog'
urlpatterns = [
    path('', home_view, name='home'),
    path('search', post_search, name='post_search'),
    path('<slug:slug>', post_detail_view, name='post_detail'),
    path('category/<str:catg>', CategoryListView.as_view(), name='category_list')
]
