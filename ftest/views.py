from django.views.generic import TemplateView, FormView, DetailView
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import CreateQuizForm
from .models import Question, Quiz, QuizSubmission, QuizQuestionAnswer


class HomeView(TemplateView):
    template_name = "ftest/home.html"


class CreateQuizView(FormView):
    template_name = "ftest/quiz_create.html"
    form_class = CreateQuizForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['questions'] = Question.objects.filter(active=True).order_by('?')[:10]

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


class QuizDetailBaseView(DetailView):
    model = Quiz

    def get_object(self):
        try:
            return Quiz.objects.get(hashid=self.kwargs['hash'])
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

        owner_answers = {str(q.question_id): q.answer for q in quiz.quizquestion_set.all()}

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
            quiz_submission.result = round(result / len(owner_answers) * 100)
            quiz_submission.save()

        return HttpResponseRedirect(
            reverse('ftest:quiz-submission', kwargs={'hash': quiz.hashid,
                                                     'pk': quiz_submission.pk}))

    def get_questions(self):
        quiz = self.object
        pronoun = 'her' if quiz.user.gender == 'female' else 'him'

        return [{
            'id': question.pk,
            'pk': question.pk,
            'options': question.options,
            'question': question.question_with_template.format(
                username=quiz.user.username,
                pronoun=pronoun
            )
        } for question in quiz.questions.filter(active=True)]


class QuizSubmissionView(DetailView):
    model = QuizSubmission
    template_name = 'ftest/quiz_submission.html'

    def get_object(self, queryset=None):
        try:
            return QuizSubmission.objects.get(pk=self.kwargs['pk'], quiz__hashid=self.kwargs['hash'])
        except QuizSubmission.DoesNotExist:
            raise Http404
