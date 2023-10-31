from django.db import models
from django.contrib.auth.models import User
# Create your models here.
def user_directory_path(instance, filename) :
    return 'user_{0}/{1}' .format(instance.user.id,filename)


class Story(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to=user_directory_path)
    caption=models.CharField(max_length=300)  # Corrected typo here
    created_at=models.DateTimeField(auto_now_add=True)