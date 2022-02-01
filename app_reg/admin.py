from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ["published_news_view"]

    list_filter = ["user", "city"]
    list_display, list_display_links = (["user", "tel", "city", "published_news_view"],) * 2

    def published_news_view(self, obj):
        return obj.published_news_count()

    # Настройки админки
    published_news_view.short_description = "Кол-во опубликованных новостей"
