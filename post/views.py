from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .models import Tag,Stream,Follow,Post,Likes
from django.contrib.auth. decorators import login_required
from .forms import NewPostForm
from django.urls import reverse
from userauths.models import Profile
from story.models import Story
from comment.forms import CommentForm
from comment.models import Comment
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.models import User

# Create your views here.
@login_required
def index(request):
    user=request.user#when display all user the code is under

    # posts=Stream.objects.filter(user=user)
    # group_ids=[]#here is change=>[post.post_id for post in posts]
    # for post in posts:
    #     group_ids.append(post.post_id)
    # # post_item=Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    # posts=Post.objects.order_by('-posted')
    all_user=User.objects.all()

     # Get the users that the current user is following
    following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)

    # Get posts from the users the current user follows
    posts = Post.objects.filter(Q(user=user) | Q(user__in=following_users)).order_by('-posted')
     # Get stories from the following users
    following_stories = Story.objects.filter(user__in=following_users)
    stories = Story.objects.all()




    context={'post_item':posts,'all_user':all_user,'following_stories':following_stories,'stories':stories}#post_item
    return render(request,'index.html',context)



def create_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data['picture']
            caption = form.cleaned_data['caption']
            tags = form.cleaned_data['tag'].split(',')  # Split tags by commas

            # Create a new post
            post = Post(picture=picture, caption=caption, user=request.user)
            post.save()

            # Add tags to the post
            for tag in tags:
                post.tag.create(title=tag.strip())  # Strip whitespace from tags

            return redirect('index')  # Redirect to the index page after successful submission
           
    else:
        form = NewPostForm()  # If it's not a POST request, create a new form instance

    context = {'form': form}
    return render(request, 'newpost.html', context)


def PostDetails(request,post_id):
    post=get_object_or_404(Post,id=post_id)

    #comment
    comments=Comment.objects.filter(post=post).order_by('date')

    #comment form
    if request.method == 'POST':
        form=CommentForm(request.POST,request.FILES)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.user=request.user
            new_comment.save()
            return redirect('post-details',post_id=post_id)#measure changes
    else:
            form=CommentForm()
    
    contex={'post':post,
            'form':form,
            'comments':comments
        }
    return render(request,'post-details.html',contex)


def tag_list(request,tag_slug):
    tag=get_object_or_404(Tag,slug=tag_slug)
    posts=Post.objects.filter(tag=tag).order_by('-posted')
    tags = Tag.objects.all()  
    context={'tags': tags,'posts':posts,'tag':tag}
    return render(request, 'tags.html', context)


def like(request,post_id):
    user=request.user
    post=Post.objects.get(id=post_id)
    current_likes=post.like 
    liked=Likes.objects.filter(user=user,post=post,).count()
    if not liked:
        liked=Likes.objects.create(user=user,post=post)
        current_likes=current_likes + 1
    else:
        liked=Likes.objects.filter(user=user,post=post).delete()
        current_likes=current_likes - 1

    post.like=current_likes
    post.save()
    return redirect('post-details', post_id=post.id)

def favourite(request,post_id):
    user=request.user
    post=get_object_or_404(Post,id=post_id)
    # profile=Profile.objects.get(user=user)
    profile = user.profile 
    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-details',args=[str(post_id)]))

# views.py
from django.shortcuts import render
from userauths.models import Profile

def saved_posts(request, username):
    user_profile = Profile.objects.get(user__username=username)
    saved_posts = user_profile.favourite.all()  # Assuming 'favourite' is a ManyToManyField to 'Post' in the Profile model

    context = {
        'user_profile': user_profile,
        'saved_posts': saved_posts,
    }
    return render(request, 'saved_posts.html', context)





























    # # # Get the newly created post (if available) from query parameters
    # # new_post_id = request.GET.get('post_id')#add
    # # if new_post_id:#add
    # #     new_post = get_object_or_404(Post, id=new_post_id)#add
    # #     post_item = [new_post] + list(post_item)  # Add the new post to the beginning of the list
    # # Check if post_id is provided in the URL
    # if post_id:
    #     try:
    #         new_post = Post.objects.get(id=post_id)
    #         post_item = [new_post] + list(post_item)  # Add the new post to the beginning of the list
    #     except Post.DoesNotExist:
    #         raise Http404("Post does not exist")


#create post

 #  # Redirect to the index page
            # index_url = reverse('index')
            # # Redirect to the user's profile page
            # profile_url = reverse('profile', args=[request.user.username])

            # return HttpResponseRedirect(f"{index_url}?post_id={post.id}&profile_url={profile_url}")
