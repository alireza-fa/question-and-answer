from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

from qanda.managers import IsActiveManager


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name=_('user'))
    subject = models.CharField(max_length=120, verbose_name=_('subject'))
    slug = models.SlugField(db_index=True, verbose_name=_('slug'), allow_unicode=True)
    body = RichTextField(verbose_name=_('body'))
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0, verbose_name=_('views'))
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.subject[:34]} - views: {self.views}'


class CategoryQuestion(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='questions', verbose_name=_('question'))
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='categories', verbose_name=_('category'))

    class Meta:
        verbose_name = _('Category Question')
        verbose_name_plural = _('Category Questions')


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', verbose_name=_('user'))
    body = RichTextField(verbose_name=_('body'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))
    likes = models.IntegerField(default=0, verbose_name=_('likes'))
    dislikes = models.ImageField(default=0, verbose_name=_('dislikes'))

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def __str__(self):
        return f'{self.user} - likes: {self.likes} dislikes: {self.dislikes}'


class QuestionSave(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='question_saves', verbose_name=_('user'))
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='user_saves', verbose_name=_('question')
    )

    class Meta:
        verbose_name = _('Question Save')
        verbose_name_plural = _('Question Saves')

    def __str__(self):
        return f'{self.user} - {self.question.subject[:34]}'


class AnswerSave(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='answer_saves', verbose_name=_('user')
    )
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name='user_saves', verbose_name=_('answer')
    )

    class Meta:
        verbose_name = _('Answer Save')
        verbose_name_plural = _('Answer Saves')

    def __str__(self):
        return f'{self.user} - answered: {self.answer.user}'
