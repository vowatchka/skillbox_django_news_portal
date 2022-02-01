from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

from app_reg.models import UserProfile

from .models import NewsArticle, Comment, Tag
from .forms import NewsArticleForm, CommentForm


def get_referer(request, default="/"):
    return request.headers.get("referer", default)


class NewsArticleList(ListView):
    model = NewsArticle
    template_name = "news-article-list.html"
    context_object_name = "news_article_list"

    def get_queryset(self):
        queryset = NewsArticle.objects.filter(activated=True)
        if tag := self.request.GET.get("tag"):
            queryset = queryset.filter(tag="#" + tag)
        return queryset.order_by("-created_date")


class NewsArticleDetail(DetailView):
    model = NewsArticle
    template_name = "news-article-detail.html"
    context_object_name = "news_article_detail"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.context_data["comments"] = self.get_object().comments.order_by("-comment_date")
        response.context_data["comment_form"] = CommentForm()

        return response

    def post(self, request, pk, *args, **kwargs):
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news_article = self.get_object()
            comment.save()
            return HttpResponseRedirect(reverse("news_article_detail", args=(pk,)))
        else:
            return render(request, self.template_name, {
                "comment_form": comment_form,
                "news_article_detail": self.get_object(),
                "comments": self.get_object().comments.order_by("-comment_date"),
            })

    @staticmethod
    @permission_required("app_news.delete_newsarticle", raise_exception=True)
    def delete_news(request, news_id, *args, **kwargs):
        news = NewsArticle.objects.get(id=news_id)
        news.delete()
        return HttpResponseRedirect("/")


class CreateNewsArticleView(PermissionRequiredMixin, TemplateView):
    template_name = "create-news-article.html"
    permission_required = ("app_news.add_newsarticle", "app_news.publish")

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.context_data["form"] = NewsArticleForm()
        response.context_data["back_uri"] = get_referer(request)
        return response

    def post(self, request, *args, **kwargs):
        form = NewsArticleForm(request.POST)

        if form.is_valid():
            news = form.save(commit=False)

            news.user = request.user
            news.save()

            if new_tags := form.cleaned_data["new_tags"]:
                new_tags = new_tags.split(" ")
                for new_tag in new_tags:
                    tag = Tag(name=new_tag)
                    tag.save()

                    news.tag.add(tag)

            news.save()

            return HttpResponseRedirect(reverse("news_article_detail", args=(news.id,)))
        else:
            return render(request, self.template_name, {"form": form})


class EditNewsArticleView(PermissionRequiredMixin, TemplateView):
    template_name = "edit-news-article.html"
    permission_required = ("app_news.change_newsarticle",)

    def get(self, request, news_id, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        news = NewsArticle.objects.get(id=news_id)

        response.context_data["form"] = NewsArticleForm(instance=news)
        response.context_data["news_id"] = news_id
        response.context_data["back_uri"] = get_referer(request)
        response.context_data["return_uri"] = response.context_data["back_uri"]
        return response

    def post(self, request, news_id, *args, **kwargs):
        news = NewsArticle.objects.get(id=news_id)
        form = NewsArticleForm(request.POST, instance=news)

        if form.is_valid():
            news = form.save(commit=False)

            if new_tags := form.cleaned_data["new_tags"]:
                new_tags = new_tags.split(" ")
                for new_tag in new_tags:
                    tag = Tag(name=new_tag)
                    tag.save()

                    news.tag.add(tag)

            news.save()

            return HttpResponseRedirect(
                request.POST["return_uri"]
                if "return_uri" in request.POST
                else reverse("news_article_detail", args(news.id, ))
            )
        else:
            return render(request, self.template_name, {"form": form, "news_id": news_id})


@permission_required("app_news.delete_comment", raise_exception=True)
def delete_comment(request, comment_id, *args, **kwargs):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponseRedirect(get_referer(request))


class UserAccount(TemplateView):
    template_name = "account.html"

    def get(self, request, user_id, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        profile = UserProfile.objects.filter(("user__id", user_id)).first()

        response.context_data["profile"] = profile

        return response
