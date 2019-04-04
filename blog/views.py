from django.db import models
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import redirect, render, get_object_or_404 
from django.utils import timezone
from taggit.models import Tag
from .forms import CommentForm, EmailPostForm, PostForm
from .models import Comment, Post
from . import readcredentials

def post_list(request, tag_slug=None):
    object_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    
    tag = None
    if tag_slug:
        tag         = get_object_or_404 (Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    
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
                  {'page' : page,
                   'posts': posts,
                   'tags' : tag   })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    
    new_comment = None
    if request.method == 'POST': # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment        = comment_form.save(commit=False)
            new_comment.post   = post # Assign the current post to the comment
            new_comment.save()        # Save the comment to the database
    else:
        comment_form = CommentForm()
    
    return render(request,
                  'blog/post_detail.html',
                  {'post'        : post,
                   'comments'    : comments,
                   'new_comment' : new_comment,
                   'comment_form': comment_form})
    

def post_edit(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post                = form.save(commit=False)
            post.author         = request.user
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
            post                = form.save(commit=False)
            post.author         = request.user
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


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status='published')
    sent = False
    
    if request.method == 'POST': # Form submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaneddata = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            subject = '{} ({}) recommends you reading "{}"'.format(cleaneddata['name'],
                                                                   cleaneddata['email'],
                                                                   post.title,)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title,
                                                                    post_url,
                                                                    cleaneddata['name'],
                                                                    cleaneddata['comments'],)
            send_mail(subject,
                      message,
                      readcredentials.readcredentials()[1],
                      [cleaneddata['to']])
            sent = True
            
    else:
        form = EmailPostForm()
    return render(request,
                  'blog/post_share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})


def about(request):
    return render(request,
                  'blog/about.html')