from django import forms
from poll.models import Question, QuestionType, Choice


class QuestionTypeForm(forms.ModelForm):

    class Meta:
        model = QuestionType
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'
