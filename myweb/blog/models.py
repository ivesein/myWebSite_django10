from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser

from django.conf import settings

from django.core.urlresolvers import reverse
# Create your models here.


class MyUser(AbstractUser):
    score = models.IntegerField(default=0)


def upload_location(instance, filename):
    PostModel = instance.__class__
    # new_id = PostModel.objects.order_by("id").last().id + 1
    """instance.__class__ gets the model Post.
    We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the
     the post we are creating.
    """
    auth = PostModel.user
    title = PostModel.title
    return "%s/%s/%s" % (auth, title, filename)


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             )
    title = models.CharField(max_length=120)
    content = models.TextField()
    publish = models.DateField(auto_now=False, auto_now_add=True)
    update = models.DateField(auto_now=True, auto_now_add=False)
    image = models.ImageField(upload_to='blogphoto',
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:details", kwargs={'id': self.id})

    class Meta:
        ordering = ["-publish", "-update"]
