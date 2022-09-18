from django.db import models
from django_hashids import HashidsField


class Question(models.Model):
    question = models.CharField(max_length=500)
    question_with_template = models.CharField(max_length=500)

    active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.question


class Quiz(models.Model):
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    )

    hashid = HashidsField(real_field_name="id", min_length=5)

    username = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    questions = models.JSONField(default={})

    active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username}: {self.get_gender_display()}'
