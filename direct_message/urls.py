from django.urls import path
from . import views

urlpatterns = [
    path('inbox/',views.index,name="inbox"),
    path('inbox/<username>/',views.Direct,name="direct"),
    path('send/',views.SendMessage,name="send-meaasge"),
    path('search/',views.UserSearch, name="user-search"),
    path('search/<username>/',views.NewMessage,name="new-message"),
]
