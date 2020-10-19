from django.urls import path
from .views import home_view, post_detail_view, CategoryListView

app_name = 'blog'
urlpatterns = [
    path('', home_view, name='home'),
    path('<slug:slug>', post_detail_view, name='post_detail'),
    path('category/<str:catg>', CategoryListView.as_view(), name='category_list')
]
