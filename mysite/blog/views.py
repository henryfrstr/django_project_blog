from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category
from .forms import NewCommentForm, PostSearchForm
from django.views.generic import ListView
from django.db.models import Q
# from django.http import HttpResponseRedirect


def home_view(request):

    post_list = Post.newmanager.all()
    paginator = Paginator(post_list, 3)

    page_number = request.GET.get('page', 1)
    print(request.GET)
    print(page_number)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {
        'posts': page_obj,
        'page_obj': page_obj,

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
        return redirect("/" + post.slug)
        # return HttpResponseRedirect(reverse("blog:post_detail", kwargs={'slug': post.slug}))
        # return HttpResponseRedirect('/' + post.slug)
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return redirect(request.META.get('HTTP_REFERER'))
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'blog/blog_detail.html', context)


class CategoryListView(ListView):
    # model = Post
    template_name = 'blog/category.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, name__iexact=self.kwargs['catg'])
        # self.category = Category.objects.get(
        #     name__iexact=self.kwargs['catg'])
        # print(self.category)
        return Post.objects.filter(category__name__iexact=self.category, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['catg'] = self.kwargs['catg']
        return context


def category_menu(request):
    category_menu = Category.objects.exclude(name__iexact='default')
    context = {
        'category_menu': category_menu
    }
    return context


def post_search(request):
    form = PostSearchForm()

    q = None
    c = None
    result = []
    query = Q()

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']
            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q)

            result = Post.objects.filter(query)

    context = {
        'form': form,
        'q': q,
        'result': result
    }
    return render(request, 'blog/search.html', context)
