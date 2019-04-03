from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db import models
from .models import Post
from .forms import PostForm
from django_extensions.db.fields import AutoSlugField

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,
                  'blog/post_list.html',
                  {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day)
    return render(request,
                  'blog/post_detail.html',
                  {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail',
                            post.get_absolute_url())
    else:
        form = PostForm()
    return render(request,
                  'blog/post_edit.html',
                  {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',
                            pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,
                  'blog/post_edit.html',
                  {'form': form})

def about(request):
    return render(request,
                  'about.html')