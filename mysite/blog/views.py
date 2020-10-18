from django.shortcuts import render, get_object_or_404
from .models import Post
# from django.http import HttpResponse


def home_view(request):

    qs = Post.newmanager.all()
    print(qs)
    context = {
        'posts': qs
    }
    return render(request, 'blog/index.html', context)


def post_detail_view(request, slug):

    post = get_object_or_404(Post, slug=slug, status='published')

    context = {
        'post': post
    }

    return render(request, 'blog/blog_detail.html', context)
