from django.db import models
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import redirect, render, get_object_or_404 
from django.utils import timezone
from .forms import PostForm
from .models import Post

def post_list(request):
    object_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(object_list, 5) # posts per page
    page = request.GET.get('page') # current page number
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    return render(request,
                  'blog/post_list.html',
                  {'page': page,
                   'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day)
    return render(request,
                  'blog/post_detail.html',
                  {'post': post})

def post_edit(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return render(request,
                          'blog/post_detail.html',
                          {'post': post})
    else:
        form = PostForm(instance=post)
    return render(request,
                  'blog/post_edit.html',
                  {'form': form})


def post_new(request, year=timezone.now().year, month=timezone.now().month, day=timezone.now().day, post=""):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return render(request,
                          'blog/post_detail.html',
                          {'post': post})
    else:
        form = PostForm()
    return render(request,
                  'blog/post_edit.html',
                  {'form': form})
    
def about(request):
    return render(request,
                  'blog/about.html')