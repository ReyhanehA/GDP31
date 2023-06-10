from django import forms
from .models import (
    Post,
    PostImage)


class CreatePostForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'What\'s the title?'}))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Sum it up in a sentence.'}))

    class Meta:
        model = Post
        fields = (
            'title',
            'description',
        )

    class Media:
        css = {
            'all': ('omblog/css/omblog.writing.css',)
        }
        js = (
            'omblog/js/jquery.autosize.js',
            'omblog/js/omblog.create.js',
        )


class PostImageForm(forms.ModelForm):

    class Meta:
        model = PostImage


class EditPostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'What\'s the title?'}))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Sum it up in a sentence.'}))
    source_content = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Now write it.'}))

    class Meta:
        model = Post
        fields = (
            'title',
            'description',
            'slug',
            'source_content',
            'status',
        )


class PostForm(forms.ModelForm):

    class Meta:
        model = Post

    class Media:
        css = {
            'all': ('omblog/css/omblog.writing.css',)
        }
        js = ('omblog/js/omblog.writing.js',)
