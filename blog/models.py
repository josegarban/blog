# Create your models here.

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset()\
               .filter(status='published').filter(published_date__lte=timezone.now())

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = RichTextUploadingField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=250,
                            unique_for_date='published_date'
                            )
    tags = TaggableManager()

    objects = models.Manager()
    publishedobjects = PublishedManager()

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        )
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) # Convert the title into a slug
        super(Post, self).save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.published_date.year,
                             self.published_date.month,
                             self.published_date.day,
                             self.slug]
                       )

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title

class Comment(models.Model): #Not used in this version
    post    = models.ForeignKey   (Post,
                                   on_delete=models.CASCADE,
                                   related_name='comments')
    name    = models.CharField    (max_length=80)
    email   = models.EmailField   ()
    body    = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active  = models.BooleanField (default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
