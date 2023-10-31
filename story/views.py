from django.shortcuts import render,redirect,get_object_or_404
from .models import Story
from .forms import StoryForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def upload_story(request):
    if request.method == "POST":
        form=StoryForm(request.POST,request.FILES)
        if form.is_valid():
            story=form.save(commit=False)
            story.user=request.user
            form.save()
            return redirect('index')
    else:
            form=StoryForm()
    context={
         'form':form,
    }
    return render(request,'story-post.html',context)




def view_user_stories(request, username):
    # Retrieve the user whose stories you want to display
    user = get_object_or_404(User, username=username)
    
    # Retrieve the stories of the user
    user_stories = Story.objects.filter(user=user)
    
    context = {
        'user': user,
        'user_stories': user_stories,
    }
    
    return render(request, 'view_stories.html', context)
