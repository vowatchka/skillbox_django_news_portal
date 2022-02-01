from django.db import models
from django.contrib.auth.models import User


class NewsArticle(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edit_date = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    activated = models.BooleanField(default=True, verbose_name="Опубликовано")
    tag = models.ManyToManyField("Tag", verbose_name="Тэги")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None,
                             verbose_name="Автор новости")

    class Meta:
        permissions = (
            ("publish", "Может опубликовать"),
        )

    def __str__(self):
        return self.title

    @property
    def comments(self):
        return Comment.objects.filter(news_article_id=self.id)

    @property
    def comments_count(self):
        return self.comments.count()

    @property
    def short_description(self):
        if len(self.content) > 150:
            return self.content[:150] + "..."
        else:
            return self.content


class Comment(models.Model):
    user_name = models.CharField(max_length=100, verbose_name="Автор комментария")
    message = models.TextField(verbose_name="Комментарий")
    comment_date = models.DateTimeField(auto_now=True, verbose_name="Дата комментария")
    news_article = models.ForeignKey("NewsArticle", on_delete=models.CASCADE, verbose_name="Прокомментированные новости")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name="Автор комментария")

    def __str__(self):
        return "%s commented by %s" % (self.news_article, self.user_name)

    def save(self):
        if self.user is not None:
            self.user_name = self.user.username
        else:
            self.user_name = self.user_name + " (аноним)"

        return super().save()


class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True, unique=True, verbose_name="Тэг")

    def __str__(self):
        return self.name
