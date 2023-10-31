from django.urls import path
from .import views

urlpatterns = [
    path('story/',views.upload_story,name="story"),
    path('user_stories/<str:username>/', views.view_user_stories, name='view_user_stories'),

]
