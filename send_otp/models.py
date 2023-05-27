from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



class PostModel(models.Model):
   
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modifiled = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        
        return f'{self.owner}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(PostModel, self).save(*args, **kwargs)
