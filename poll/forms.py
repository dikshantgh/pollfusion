from django import forms
from poll.models import Question, QuestionType, Choice,Contact


class QuestionTypeForm(forms.ModelForm):

    class Meta:
        model = QuestionType
        fields = '__all__'


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        exclude =['hit_ques']
        fields = '__all__'
        
        
class ChoiceForm(forms.ModelForm):
    # error_messages = {
    #         'required': 'my custom error message',
    #     }
    class Meta:
        

        model = Choice
        exclude =['votes']
        fields = '__all__'
        # widgets = {'choice_text': forms.RadioSelect()}

        
class ContactForm(forms.ModelForm):
   

       # name = forms.CharField(help_text="nameplzz")
    class Meta:
        model = Contact
        fields = '__all__'