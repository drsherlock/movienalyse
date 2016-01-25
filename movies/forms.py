from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Review, Forum, Body


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        exclude = ['movie_id', 'user_id']

class TopicForm(forms.ModelForm):
    class Meta:
        model  = Forum
        fields = ['topic']


# class MoveNodeForm(forms.ModelForm):
#     target = TreeNodeChoiceField(queryset=Body.objects.all())
#     position = 'right'
#     class Meta:
#         model = Body
#         fields = ['comment']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Body
        # if flag = 0:
        #     fields = ('comment', 'forum', 'parent')
        # else:
        #     fields = ('comment')

        # widgets = {
        #     'comment': forms.Textarea,
        #     'forum': forms.HiddenInput,
        #     'parent': forms.HiddenInput,
        # }
        fields = ['comment']

    # def save(self, *args, **kwargs):
    #     self.parent = self.cleaned_data['parent']
    #     return super(CommentForm, self).save(*args, **kwargs)
