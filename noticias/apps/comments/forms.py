# -*- coding: utf-8 -*-
from django import forms
from django.contrib.comments.models import Comment
from captcha.fields import CaptchaField

class CommentForm(forms.ModelForm):

    user_name = forms.CharField(label=u'Nome')
    user_email = forms.EmailField(label=u'E-mail')
    comment = forms.Field(label=u'Comentário',widget=forms.Textarea)
    captcha = CaptchaField()
    class Meta:
        model = Comment
        fields = ('user_name','user_email','comment','submit_date')
        exclude = "submit_date",

