from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from post.models import Post,Follow,Stream
from story.models import Story
from django.urls import resolve
from .models import Profile
from .forms import EditProfileForm,UserRegisterForm
from django.contrib.auth import login,authenticate
from django.contrib import messages

@login_required
def userProfile(request,username):
    user=get_object_or_404(User,username=username)
    user_stories = Story.objects.filter(user=user)

    profile = Profile.objects.get(user=user)
    url_name=resolve(request.path).url_name
    if url_name == 'profile':
        posts=Post.objects.filter(user=user).order_by('-posted')
    else:
        posts=profile.favourite.all()

    follow_status =Follow.objects.filter (following=user,follower=request.user).exists()

    #treakng status
    post_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    Followers_count= Follow.objects.filter(following=user).count()

    posts = Post.objects.filter(user=user).order_by('-posted')
    context = {
        'posts': posts,
        'profile': profile,
        'user': user,
        'follow_status': follow_status,
        'post_count': post_count,
        'following_count':following_count,
        'Followers_count': Followers_count,
        'user_stories':user_stories,
    }
    return render(request, 'profile.html', context)
                



def follow(request,username, option):
    user=request.user
    following = get_object_or_404(User, username=username)
    try: 
        f,created = Follow.objects.get_or_create(follower=user,following=following)
        if int(option) == 0:
            f. delete()
            Stream. objects. filter (following=following, user=user).all().delete()
        else:
            posts = Post. objects. filter (user=following)[:10]


            with transaction. atomic():
                for post in posts:
                    stream = Stream (post=post, user=user, date=post.posted,following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User. DoesNotExist:
        return HttpResponseRedirect(reverse( 'profile', args=[username]))



def editProfile(request):
    user=request.user.id
    profile=Profile.objects.get(user_id=user)
    if request.method == "POST":
        form=EditProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile.image=form.cleaned_data.get('image')
            profile.first_name=form.cleaned_data.get('first_name')
            profile.last_name=form.cleaned_data.get('last_name')
            profile.bio=form.cleaned_data.get('bio')
            profile.location=form.cleaned_data.get('location')
            # profile.url=form.cleaned_data.get('url')
            profile.save()
            return redirect('profile', username=profile.user.username)

    else:
        form=EditProfileForm()
    context={
        'form':form
    }
    return render(request,'edit_profile.html',context)



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Profile.get_or_create(user=request.user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hurray your account was created!!')

            # Automatically Log In The User
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            # return redirect('editprofile')
            return redirect('index')
                       

            


    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request,'sign-up.html',context)




