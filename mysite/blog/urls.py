from django.urls import path
from .views import home_view, post_detail_view

app_name = 'blog'
urlpatterns = [
    path('', home_view, name='home'),
    path('<slug:slug>', post_detail_view, name='post_detail')
]
