from django.dispatch import Signal, receiver

from misago.categories.models import PRIVATE_THREADS_ROOT
from misago.categories.signals import delete_category_content, move_category_content
from misago.threads.signals import merge_thread, move_thread, merge_post, move_post


thread_read = Signal(providing_args=["thread"])


@receiver(delete_category_content)
def delete_category_threads(sender, **kwargs):
    sender.postread_set.all().delete()


@receiver(move_category_content)
def move_category_tracker(sender, **kwargs):
    sender.postread_set.update(category=kwargs['new_category'])


@receiver(merge_thread)
def merge_thread_tracker(sender, **kwargs):
    other_thread = kwargs['other_thread']
    other_thread.postread_set.update(
        category=sender.category,
        thread=sender,
    )


@receiver(move_thread)
def move_thread_tracker(sender, **kwargs):
    sender.postread_set.update(
        category=sender.category,
        thread=sender,
    )


@receiver(merge_post)
def merge_post_delete_tracker(sender, **kwargs):
    sender.postread_set.all().delete()


@receiver(move_post)
def move_post_delete_tracker(sender, **kwargs):
    sender.postread_set.all().delete()


@receiver(thread_read)
def decrease_unread_private_count(sender, **kwargs):
    user = sender
    thread = kwargs['thread']

    if thread.category.thread_type.root_name != PRIVATE_THREADS_ROOT:
        return

    if user.unread_private_threads:
        user.unread_private_threads -= 1
        user.save(update_fields=['unread_private_threads'])
