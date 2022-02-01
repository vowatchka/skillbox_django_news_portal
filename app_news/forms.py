from django import forms

from .models import NewsArticle, Comment


class NewsArticleForm(forms.ModelForm):
    new_tags = forms.CharField(max_length=100, required=False, label="Добавить тэги (через пробел)")

    class Meta:
        model = NewsArticle
        fields = ["activated", "title", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["user_name", "user", "message"]
