from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Post
from .forms import NewCommentForm
from django.http import HttpResponseRedirect


def home_view(request):

    qs = Post.newmanager.all()
    print(qs)
    context = {
        'posts': qs
    }
    return render(request, 'blog/index.html', context)


def post_detail_view(request, slug):

    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(status=True)
    user_comment = None
    comment_form = NewCommentForm(request.POST or None)

    if comment_form.is_valid():
        user_comment = comment_form.save(commit=False)
        user_comment.post = post
        user_comment.save()
        # return redirect("blog:post_detail", slug=post.slug)
        # return redirect("/" + post.slug)
        # return HttpResponseRedirect(reverse("blog:post_detail", kwargs={'slug': post.slug}))
        # return HttpResponseRedirect('/' + post.slug)
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get('HTTP_REFERER'))
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'blog/blog_detail.html', context)
