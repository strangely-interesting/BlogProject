from django.contrib import admin
from Blog import models

# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.PostImage)
admin.site.register(models.PostLike)
admin.site.register(models.PostComment)