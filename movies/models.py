from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.core import urlresolvers
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

class Movie(models.Model):
    title = models.CharField(max_length=128, blank=False)
    description = models.TextField()
    movie_length = models.CharField(max_length=20)
    director = models.CharField(max_length=50)
    rating = models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(10.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='movie_img/')
    category = models.CharField(max_length=50)
    movie_pts = models.FloatField()
    trailers = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return (self.title)

class Review(models.Model):
    rating = models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(10.0)], default="0.0")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def set_movie_rtngs(self):
        movie_obj = self.movie_id
        review_objs = movie_obj.review_set.all()
        total_reviews = review_objs.count()
        total_rtngs = 0
        for obj in review_objs:
            total_rtngs = total_rtngs + obj.rating
        new_rtng = total_rtngs/total_reviews
        movie_obj.rating = new_rtng
        movie_obj.save()


class Forum(models.Model):
    topic = models.CharField(max_length=500)
    started_by = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.topic)

    class Meta:
      get_latest_by = 'created_at'

class Body(MPTTModel):
    forum = models.ForeignKey(Forum)
    comment = models.TextField(max_length=2000)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.comment)

    def set_movie_pts(self):
        one_day = timezone.now().date() - timedelta(days=1)
        ten_days = timezone.now().date() - timedelta(days=10)
        hundred_days = timezone.now().date() - timedelta(days=100)

        movie_obj = self.forum.movie_id

        forum_objs = movie_obj.forum_set.all()

        total = 0

        for obj in forum_objs:
            one = obj.body_set.filter(created_at__gte=one_day).count()/1
            ten = obj.body_set.filter(created_at__gte=ten_days).count()/10
            hundred = obj.body_set.filter(created_at__gte=hundred_days).count()/100
            total = total + one + ten + hundred


        # one = self.forum_set.movie_id.body_set.filter(created_at__gte=one_day).count()/1
        # ten = self.forum_set.movie_id.body_set.filter(created_at__gte=ten_days).count()/10
        # hundred = self.forum_set.movie_id.body_set.filter(created_at__gte=hundred_days).count()/100

        movie_obj.movie_pts = total
        movie_obj.save()


    class Meta:
      get_latest_by = 'created_at'

    # def get_absolute_url(self):
    #     return reverse('posting_detail', kwargs={'pk': self.forum.id})

    # def save(self, *args, **kwargs):
    #     super(Body, self).save(*args, **kwargs)
    #     assign_perm('postings.delete_postingcomment', self.user, self)
    #     return

    # class MPTTMeta:
    #     order_insertion_by = ['created_at']
