from django.contrib.auth.models import User
from django.db import models

from app_news.models import NewsArticle

class UserProfile(models.Model):
    tel = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    city = models.CharField(max_length=100, blank=True, verbose_name="Город")
    published_news = models.IntegerField(default=0, verbose_name="Кол-во опубликованных новостей")
    # verificated = models.BooleanField(default=False, verbose_name="Верификация")

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    def published_news_count(self):
        return NewsArticle.objects.filter(user=self.user, activated=True).count()
