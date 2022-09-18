from django.urls import path

from .views import *

app_name = "ftest"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('create/', CreateQuizView.as_view(), name="create-quiz"),
]
