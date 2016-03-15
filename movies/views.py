from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Movie, Review, Forum, Body
from .forms import ReviewForm, TopicForm, CommentForm
import simplejson as json
from haystack.query import SearchQuerySet




def show_home(request):
    top_movies = Movie.objects.all().order_by('-movie_pts')[:10]
    context={
        "movies":top_movies
    }

    return render(request, "home.html",context)

def show_list(request):
    sort_by = request.GET.get('sort')
    if sort_by == 'rating':
        object = Movie.objects.all().order_by('-rating')
    elif sort_by == 'name':
        object = Movie.objects.all().order_by('title')
    else:
        object = Movie.objects.all()
    
    context={
        "object":object
    }
    return render(request,'allMovies.html',context)

def show_detail(request, id):
    context = {}
    object = Movie.objects.get(pk=id)
    review = Review.objects.filter(movie_id=id).order_by('-created_at')
    forum = Forum.objects.filter(movie_id=id)
    trailer_list = object.trailers.split(',')
    context={
        "object":object,
        "review":review,
        "forum":forum,
        "trailer_list":trailer_list
        
    }
    return render(request, "detail.html", context)

def show_comments(request, id1, id2):
    context = {}
    title = Forum.objects.get(pk=id2)

    nodes = Body.objects.filter(forum__pk=id2)
    context={
        "title":title,
        "nodes":nodes,
    }
    return render(request, "forumComments.html", context)

def new_review(request, id):
    if(request.user.is_authenticated()):
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            movie_id = Movie.objects.get(pk=id)
            user_id = User.objects.get(username=request.user)
            data = form.save(commit=False)
            data.movie_id = movie_id
            data.user_id = user_id
            full_name = form.cleaned_data.get("user_id")
            data.save()

            data.set_movie_rtngs()

            direct = '/movie/'+id+'/'
            return HttpResponseRedirect(direct)
        context={
            "form":form
        }
        return render(request,'userReview.html',context)
    else:
        return redirect('/accounts/login')

def new_topic(request, id):
    if(request.user.is_authenticated()):
        if request.method == 'POST':
            form = TopicForm(request.POST)
            movie_id = Movie.objects.get(pk=id)
            # try:
            #     title = Forum.objects.latest()
            #     node = title.pk + 1
            # except:
            #     node = 1

            if form.is_valid():
                instance = form.save(commit=False)
                instance.movie_id = movie_id
                instance.started_by = request.user
                instance.save()
                node = instance.pk
                node = str(node)
                direct = '/movie/'+id+'/forum/'+node+'/newforum'
                return HttpResponseRedirect(direct)
            context={
                "form":form,
            }
            return render(request, 'newTopic.html', context)
        else:
            form = TopicForm()
            context={
                "form":form,
            }
            return render(request,'newTopic.html', context)
    else:
        return redirect('/accounts/login')

def new_comment(request, id1, id2, id3=None):
    if(request.user.is_authenticated()):
        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user

                instance.forum = Forum.objects.get(pk=id2)
                if id3:
                    instance.parent = Body.objects.get(pk=id3)
                else:
                    instance.parent = None

                # instance.forum = instance.forum
                # instance.forum = Forum.objects.get(pk=node)

                instance.save()

                instance.set_movie_pts()

                direct = '/movie/'+id1+'/forum/'+id2+'/'
                return HttpResponseRedirect(direct)
            context={

                "form":form
            }
            return render(request,'doComment.html',context)
        else:
            form = CommentForm()
            context={
                "form":form
            }
            return render(request,'doComment.html', context)
    else:
        return redirect('/accounts/login')

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
