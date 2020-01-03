from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse #it will allows us to build urls by their name and passing optional parameters
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES=(
        ('draft','Draft'),
        ('published','Published'),
    )
    title=models.CharField(max_length=250)# it translates into varchar
    slug=models.SlugField(max_length=250,unique_for_date='publish')#this is used for building good looking urls, we have added the 
                        # unique_for_date parameter to this field so that we can build urls for posts using their publish date and slug. 
                        # django will prevent multiple posts from having the same slug for a given date.
    author=models.ForeignKey(User,on_delete=models.CASCADE
                                ,related_name='blog_posts')#many to one relationship. each post is written by a user and a user can write
                        # any number of posts.the on_delete parameter specifies the behavior to adopt when the referenced object is deleted .
                        # using cascade, we specify that when the reference user is deleted the database will also delete its related blog posts.

    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10
                                ,choices=STATUS_CHOICES
                                ,default='draft')

    objects=models.Manager()#default manager
    published=PublishedManager()#custom manager

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year
                                                    ,self.publish.month
                                                    ,self.publish.day
                                                    ,self.slug])
    
    class Meta:
        ordering=('-publish',)
    def __str__(self):
        return self.title


                                        
  