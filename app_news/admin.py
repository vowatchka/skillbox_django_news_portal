from django.contrib import admin
from django.utils.html import format_html

from .models import NewsArticle, Comment, Tag


class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    readonly_fields = ["created_date_view", "edit_date_view", "comments_count_view", "user"]
    list_filter = ["activated", "created_date", "tag"]
    list_display, \
    list_display_links = (
                             ["title", "activated", "tag_view", "short_description_view", "comments_count_view",
                              "created_date_view", "edit_date_view"],
                         ) * 2

    inlines = [CommentsInline]

    actions = ["activate", "deactivate"]

    def created_date_view(self, obj):
        return obj.created_date.strftime("%d.%m.%Y %H:%M:%S")

    def edit_date_view(self, obj):
        return obj.edit_date.strftime("%d.%m.%Y %H:%M:%S")

    def short_description_view(self, obj):
        return obj.short_description

    def comments_count_view(self, obj):
        return obj.comments_count

    def tag_view(self, obj):
        return "\n".join([tag.name for tag in obj.tag.all()])

    def activate(self, request, queryset):
        queryset.update(activated=True)

    def deactivate(self, request, queryet):
        queryet.update(activated=False)

    # Настройки админки
    created_date_view.short_description = "Дата создания"
    edit_date_view.short_description = "Дата изменения"
    short_description_view.short_description = "Аннотация"
    comments_count_view.short_description = "Кол-во комментариев"
    tag_view.short_description = "Тэги"

    # Групповые действия
    activate.short_description = "Опубликовать"
    deactivate.short_description = "Снять с публикации"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ["comment_date_view"]
    list_filter = ["user_name"]
    list_display, \
    list_display_links = (
                             ["user_name", "short_message", "comment_date_view", "news_article_link"],
                         ) * 2

    actions = ["delete_by_admin"]

    def comment_date_view(self, obj):
        return obj.comment_date.strftime("%d.%m.%Y %H:%M:%S")

    def short_message(self, obj):
        if len(obj.message) > 150:
            return obj.message[:150] + "..."
        else:
            return obj.message

    def news_article_link(self, obj):
        # Не занимался вопросом, как не хардкодить в урле
        # app_news и newsarticle.
        return format_html(
            '<a href="/admin/app_news/newsarticle/{}/change/">{}</a>',
            obj.news_article.id,
            obj.news_article
        )

    def delete_by_admin(self, request, queryset):
        queryset.update(message="Удалено администратором")

    # Настройки админки
    comment_date_view.short_description = "Дата комментария"
    short_message.short_description = "Комментарий"
    news_article_link.short_description = "Прокомментированные новости"

    # Групповые действия
    delete_by_admin.short_description = 'Текст комментария = "Удалено администратором"'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_filter = ["name"]
    list_display, list_display_links = (["name"],) * 2
