from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Movie ,Review, Forum, Body


class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    class Meta:
        model = Movie

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["rating", "comment", "movie_id", "user_id", "created_at"]
    class Meta:
        model = Review

class BodyAdmin(MPTTModelAdmin):
    list_display = ["comment", "parent", "forum", "author", "created_at"]
    class Meta:
        model = Body

class ForumAdmin(admin.ModelAdmin):
    list_display = ["topic", "movie_id", "started_by", "created_at"]
    class Meta:
        model = Forum


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Body, BodyAdmin)
