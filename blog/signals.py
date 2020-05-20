import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Post


@receiver(post_delete, sender=Post)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes images from filesystem
    when corresponding `Post` object is deleted.
    """
    if instance.images:
        if os.path.isfile(instance.images.path):
            os.remove(instance.images.path)


@receiver(pre_save, sender=Post)
def auto_delete_image_on_change(sender, instance, **kwargs):
    """
    Deletes old images from filesystem
    when corresponding `Post` object is updated
    with new images.
    """
    if not instance.pk:
        return False

    old_image = Post.objects.get(pk=instance.pk).images

    if Post.objects.get(pk=instance.pk).images:
        new_image = instance.images
        if not old_image == new_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)
