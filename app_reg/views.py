from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import RegisterForm
from .models import UserProfile


class RegisterView(TemplateView):
    template_name = "register.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.context_data["reg_form"] = RegisterForm()
        return response

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if form.is_valid():
            form_user = form.save()

            username = form.cleaned_data.get("username")
            raw_pass = form.cleaned_data.get("password1")

            user = authenticate(username=username, password=raw_pass)
            login(request, user)

            UserProfile.objects.create(
                user=form_user,
                tel=form.cleaned_data.get("tel"),
                city=form.cleaned_data.get("city")
            )

            return redirect("/")
        else:
            return render(request, self.template_name, {"reg_form": form})
