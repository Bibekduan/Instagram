from django.contrib import admin
from .models import Tag,Stream,Post,Follow

# Register your models here.
admin.site.register(Tag)
admin.site.register(Stream)
admin.site.register(Post)
admin.site.register(Follow)

