from django.db import models


class Likes(models.Model):
    user_hash = models.CharField(max_length=255)
    resource = models.ForeignKey(
        'resources.ResourcePage',
        # When resource is deleted, delete the likes as well
        on_delete=models.CASCADE,
    )
    like_value = models.IntegerField()
