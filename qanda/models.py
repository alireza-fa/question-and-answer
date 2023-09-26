from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name=_('user'))
    subject = models.CharField(max_length=120, verbose_name=_('subject'))
    slug = models.SlugField(db_index=True, verbose_name=_('slug'), allow_unicode=True)
    body = RichTextUploadingField(verbose_name=_('body'))
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0, verbose_name=_('views'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_show = models.BooleanField(default=False, verbose_name=_('is show'))

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.subject[:34]} - views: {self.views}'


class Answer(models.Model):
    pass
