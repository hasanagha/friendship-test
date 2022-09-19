from django.db import models
from django.urls import reverse
from django_hashids import HashidsField
from ftest.constants import GENDER_MALE, GENDER_FEMALE


class Question(models.Model):
    question = models.CharField(max_length=500)
    question_with_template = models.CharField(max_length=500)

    options = models.JSONField(default=dict)

    active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.question


class QuizUser(models.Model):
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    )

    username = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Quiz(models.Model):
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE, related_name='user_quiz')
    hashid = HashidsField(real_field_name="id", min_length=7)

    questions = models.ManyToManyField(Question, through='ftest.QuizQuestion')

    active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.hashid}: {self.user}'

    def get_quiz_url(self):
        return reverse('ftest:quiz-view', kwargs={'hash': self.hashid})


class QuizSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE)

    result = models.IntegerField(default=0)

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.quiz}'


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return f'Q:{self.quiz} > {self.question}'


class QuizQuestionAnswer(models.Model):
    submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE, related_name="submission_answers", null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_answers", null=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return f'S:{self.submission}: Q:{self.quiz} > {self.question}'
