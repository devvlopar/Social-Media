from django.db import models

# Create your models here.

class User(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    bio = models.CharField(max_length=60, null=True, blank=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    profession = models.CharField(max_length=20, null=True, blank=True)
    pic = models.FileField(upload_to='profile',default='avtar.png')
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        return self.fullname


class Post(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    private_status = models.BooleanField(default=False)
    hashtag = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True,blank=True)
    pic = models.FileField(upload_to='posts',null=True,blank=True)
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    comment_count = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.caption)


class Comment(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text