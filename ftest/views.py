from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.views.generic import TemplateView, FormView, DetailView

from ftest.forms import CreateQuizForm
from ftest.constants import PRONOUN_MALE, PRONOUN_FEMALE, GENDER_FEMALE
from ftest.models import Question, Quiz, QuizSubmission, QuizQuestionAnswer


class HomeView(TemplateView):
    template_name = "ftest/home.html"


class CreateQuizView(FormView):
    template_name = "ftest/quiz_create.html"
    form_class = CreateQuizForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['questions'] = self.get_questions()

        return ctx

    def form_valid(self, form):
        user = form.save()
        form_data = form.data
        quiz = Quiz.objects.create(user=user)

        for qid, answer in form_data.items():
            if qid in ['username', 'gender', 'csrfmiddlewaretoken']:
                continue

            try:
                question = Question.objects.get(pk=qid)
                quiz.questions.add(question, through_defaults={'answer': answer})
            except Question.DoesNotExist:
                pass

        quiz.save()

        return HttpResponseRedirect(reverse('ftest:quiz-success', kwargs={'hash': quiz.hashid}))

    def get_questions(self, count=10):
        return Question.objects.filter(active=True).values("id", "question", "options").order_by('?')[:count]


class QuizDetailBaseView(DetailView):
    model = Quiz

    def get_object(self):
        try:
            return Quiz.objects.select_related('user').get(hashid=self.kwargs['hash'])
        except Quiz.DoesNotExist:
            raise Http404


class QuizSuccessView(QuizDetailBaseView):
    template_name = 'ftest/quiz_success.html'
    model = Quiz


class QuizView(QuizDetailBaseView, FormView):
    template_name = 'ftest/quiz_view.html'
    form_class = CreateQuizForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['questions'] = self.get_questions()

        return ctx

    def form_valid(self, form):
        user = form.save()
        form_data = form.data
        quiz = self.get_object()
        quiz_submission = QuizSubmission.objects.create(user=user, quiz=quiz)

        result = 0

        owner_answers = {str(q['question_id']): q['answer'] for q in quiz.quizquestion_set.all().values('question_id', 'answer')}

        for qid, answer in form_data.items():
            if qid in ['username', 'gender', 'csrfmiddlewaretoken']:
                continue

            try:
                question = Question.objects.get(pk=qid)
                QuizQuestionAnswer.objects.create(submission=quiz_submission, question=question, answer=answer)
            except Question.DoesNotExist:
                pass

            # matching answer with owner's answer
            owner_answer_to_this_question = owner_answers[qid]
            if owner_answer_to_this_question == answer:
                result += 1

        if result:
            quiz_submission.result = self.get_results(result, len(owner_answers))
            quiz_submission.save()

        return HttpResponseRedirect(
            reverse('ftest:quiz-submission', kwargs={'hash': quiz.hashid,
                                                     'pk': quiz_submission.pk}))

    def get_results(self, total_matched, total_questions):
        return round(total_matched / total_questions * 100)

    def get_questions(self):
        quiz = self.object
        pronoun = PRONOUN_FEMALE if quiz.user.gender == GENDER_FEMALE else PRONOUN_MALE

        return [{
            'id': question.pk,
            'pk': question.pk,
            'options': question.options,
            'question': question.question_with_template.format(
                username=quiz.user.username.title(),
                pronoun=pronoun
            )
        } for question in quiz.questions.filter(active=True)]


class QuizSubmissionView(DetailView):
    model = QuizSubmission
    template_name = 'ftest/quiz_submission.html'

    def get_object(self, queryset=None):
        try:
            return QuizSubmission.objects.select_related('quiz').get(pk=self.kwargs['pk'], quiz__hashid=self.kwargs['hash'])
        except QuizSubmission.DoesNotExist:
            raise Http404
