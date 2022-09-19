import json

from django.urls import reverse
from django.conf import settings
from django.test import TestCase

from ftest.models import *
from ftest.views import CreateQuizView, QuizView


class TestViews(TestCase):
    def setUp(self):
        self.user_1 = QuizUser.objects.create(username='john', gender='male')
        self.user_2 = QuizUser.objects.create(username='nina', gender='female')

        sample_json = [
            {"question": "Q1", "options": ["A1-1", "A1-2"]},
            {"question": "Q2", "options": ["A2-1", "A2-2"]},
            {"question": "Q3", "options": ["A3-1", "A2-2"]},
            {"question": "Q4", "options": ["A4-1", "A4-2"]},
        ]

        self.q1 = Question.objects.create(question=sample_json[0]['question'], options=sample_json[0]['options'])
        self.q2 = Question.objects.create(question=sample_json[1]['question'], options=sample_json[1]['options'])
        self.q3 = Question.objects.create(question=sample_json[2]['question'], options=sample_json[2]['options'])
        self.q4 = Question.objects.create(question=sample_json[3]['question'], options=sample_json[3]['options'])

        self.quiz = Quiz.objects.create(user=self.user_1)
        self.quiz.questions.add(self.q1, through_defaults={'answer': 'A1-1'})
        self.quiz.questions.add(self.q2, through_defaults={'answer': 'A2-1'})

    def test_questions_from_db(self):
        """
        Ensure We get required record counts from db
        """
        questions = CreateQuizView.get_questions(self)

        self.assertEqual(questions.count(), 4)

    def test_each_time_we_get_random_questions(self):
        """
        Ensure we get random questions everytime.
        """
        questions_set_1 = [i['pk'] for i in CreateQuizView.get_questions(self, 2).values('pk')]
        questions_set_2 = [i['pk'] for i in CreateQuizView.get_questions(self, 2).values('pk')]

        difference = list(set(questions_set_1) - set(questions_set_2))
        print(difference)

        self.assertTrue(len(difference) != 0)

    def test_quiz_calculation_0_percent(self):
        r = QuizView.get_results(self, total_matched=0, total_questions=4)

        self.assertEqual(0, r)

    def test_quiz_calculation_25_percent(self):
        r = QuizView.get_results(self, total_matched=1, total_questions=4)

        self.assertEqual(25, r)

    def test_quiz_calculation_50_percent(self):
        r = QuizView.get_results(self, total_matched=2, total_questions=4)

        self.assertEqual(50, r)

    def test_quiz_calculation_25_percent(self):
        r = QuizView.get_results(self, total_matched=4, total_questions=4)

        self.assertEqual(100, r)
