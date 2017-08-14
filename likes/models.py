from django.db import models

class Likes(models.Model):
    user_hash = models.CharField(max_length=255)
    resource = models.ForeignKey(
        'resources.ResourcePage',
        on_delete=models.CASCADE, # When resource is deleted, delete the likes as well
    )
    like_value = models.IntegerField()
