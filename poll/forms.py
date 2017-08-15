from django import forms
from poll.models import Question, QuestionType, Choice


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
        #widgets = {'choice_text': forms.CheckboxInput()}

        # def __init__(self,*args,**kwargs):
        #     super(ChoiceForm,self).__init__(*args,**kwargs)
        #     self.error_messages['required']
        # def __init__(self, *args, **kwargs):
        #     super(ChoiceForm, self).__init__(*args, **kwargs)
        #     for k, field in self.fields.items():
        #         if 'fill' in field.error_messages:
        #             field.error_messages['fill'] = 'You have to fill this.'


    # def __init__(self,*args,**kwargs):
    #     super(ChoiceForm,self).__init__(*args,**kwargs)
    #     self.fields['choice_text'].error_messages = {'required': 'FAS:DJFASKL:DJF'}
        
    #     # 