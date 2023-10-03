from django.contrib import admin

from qanda.models import Category, Question


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name_en',)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
