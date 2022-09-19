from django.urls import path

from .views import *

app_name = "ftest"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('quiz/create/', CreateQuizView.as_view(), name='quiz-create'),
    path('quiz/<str:hash>/', QuizView.as_view(), name='quiz-view'),
    path('quiz/<str:hash>/success/', QuizSuccessView.as_view(), name='quiz-success'),
    path('quiz/<str:hash>/<int:pk>/', QuizSubmissionView.as_view(), name='quiz-submission'),
]
