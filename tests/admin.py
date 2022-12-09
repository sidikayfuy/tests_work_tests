from django.contrib import admin
from django import forms
from django.template.loader import get_template
from django.utils.functional import cached_property
from nested_admin import nested

from .models import Test, Question, Answer, Result


class AnswerAdminInline(nested.NestedStackedInline):
    extra = 1
    model = Answer


class QuestionAdminInline(nested.NestedStackedInline):
    extra = 1
    model = Question
    inlines = [AnswerAdminInline]


class TestAdmin(nested.NestedModelAdmin):
    model = Test
    inlines = [QuestionAdminInline]


admin.site.register(Test, TestAdmin)



