from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('create_post/',views.create_post,name="create_post"),
    path('post-details/<uuid:post_id>/',views.PostDetails,name="post-details"),
    path('tags/<slug:tag_slug>/', views.tag_list, name='tags'),
    path('like/<uuid:post_id>/',views.like,name="like"),
    path('favourite/<uuid:post_id>/', views.favourite, name="post.favourite"),
    path('<username>/saved/', views.saved_posts, name='favourite'),


]
