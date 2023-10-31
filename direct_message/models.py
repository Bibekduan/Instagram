from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
# Create your models here.
class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="from_user")
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name="to_user")
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)


    #sender message
    def send_message(from_user,to_user,body):
        #sender message function
        sender_message=Message(
            user=from_user,
            sender=from_user,
            receiver=to_user,
            body = body,
            is_read=True,
        )
        sender_message.save()

        #receiver message function
        receiver_message=Message(
            user=to_user,
            sender=from_user,#from_user
            receiver=from_user,
            body=body,
            is_read=True
        )
        receiver_message.save()
        return sender_message 
    

    def get_message(user):
        users=[]
        messages=Message.objects.filter(user=user).values("receiver").annotate(last=Max('date')).order_by("-last")
        for message in messages:
            users.append({
                'user':User.objects.get(pk=message['receiver']),
                'last':message['last'],
                'unread':Message.objects.filter(user=user,receiver__pk=message['receiver'],is_read=False).count(),
            })
        return users