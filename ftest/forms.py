from django import forms
from ftest.models import QuizUser


class CreateQuizForm(forms.ModelForm):
    class Meta:
        model = QuizUser
        fields = ('username', 'gender')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }
