from django.urls import path
from .views import NewsArticleList, NewsArticleDetail, CreateNewsArticleView, EditNewsArticleView, delete_comment, UserAccount

urlpatterns = [
    path("", NewsArticleList.as_view(), name="news_article_list"),
    path("news/<int:pk>/", NewsArticleDetail.as_view(), name="news_article_detail"),
    path("news/create/", CreateNewsArticleView.as_view(), name="create_news_article"),
    path("news/edit/<int:news_id>/", EditNewsArticleView.as_view(), name="edit_news_article"),
    path("news/delete/<int:news_id>/", NewsArticleDetail.delete_news, name="delete_news_article"),
    path("comment/delete/<int:comment_id>/", delete_comment, name="delete_comment"),
    path("account/<int:user_id>/", UserAccount.as_view(), name="account"),
]
