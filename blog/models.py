# Create your models here.

from django.conf import settings
from django.db import models
from django.utils import timezone

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=250,
                            unique_for_date='published_date'
                            )
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        )
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug]
                       )

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title
    
