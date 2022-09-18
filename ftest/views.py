from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "ftest/home.html"


class CreateQuizView(TemplateView):
    template_name = "ftest/create_quiz.html"
