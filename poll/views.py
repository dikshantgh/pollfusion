from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from poll.models import QuestionType, Question, Choice
from django.core.urlresolvers import reverse_lazy
from poll.forms import QuestionTypeForm, QuestionForm, ChoiceForm
from django.shortcuts import get_object_or_404, render
import pydoc
# Create your views here.


class QuestionTypeView(ListView):

    # lists all question type
	model = QuestionType
	template_name = "poll/main_page.html"
	form_class = QuestionTypeForm


    


class QuestionBriefView(DetailView):

    model = QuestionType
    template_name = "poll/question_list.html"
    form_class = QuestionForm
    def get_context_data(self, **kwargs):
        context = super(QuestionBriefView, self).get_context_data(**kwargs)
        context['queryset'] = Question.objects.all()
        return context

class QuestionDetailView(DetailView):

    model = Question
    template_name = "poll/question_detail.html"
    form_class = QuestionForm
    #success_url = reverse_lazy('poll:main_page')

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        ques_id = self.kwargs['pk']
        page =  Question.objects.get(id =ques_id)
        page.hit_ques = page.hit_ques + 1
        context['view'] = page.hit_ques
        page.save()
        return context
    

    

class TypeCreateView(CreateView):


    form_class = QuestionTypeForm
    template_name = "poll/create_type.html"
    success_url = reverse_lazy('poll:main_page')


class QuestionCreateView(CreateView):


    form_class = QuestionForm
    template_name = "poll/create_question.html"
    success_url = reverse_lazy('poll:main_page')

    def get_initial(self):
        initials = super(QuestionCreateView, self).get_initial()
        initials['question_type'] = self.kwargs['pk']
        return initials


class OptionCreateView(CreateView):


    form_class = ChoiceForm
    template_name = "poll/create_option.html"
    success_url = reverse_lazy('poll:main_page')

    def get_initial(self):
        initials = super(OptionCreateView, self).get_initial()
        initials['question'] = self.kwargs['pk']
        return initials
    
    
class QuestionUpdateView(UpdateView):

    model = Question
    template_name = "poll/create_question.html"
    form_class = QuestionForm
    success_url = reverse_lazy('poll:main_page')

class QuestionDeleteView(DeleteView):

    model = Question
    form_class = QuestionForm
    template_name = "poll/delete_question.html"
    success_url = reverse_lazy('poll:main_page')

class OptionDeleteView(DeleteView):

    model = Choice
    form_class = ChoiceForm
    template_name = "poll/delete_option.html"
    success_url = reverse_lazy('poll:main_page')


class OptionUpdateView(UpdateView):

    model = Choice
    template_name = "poll/create_option.html"
    form_class = ChoiceForm
    success_url = reverse_lazy('poll:main_page')



class ResultDisplayView(DetailView):            # to display the final results

   # form_class = ChoiceForm
    template_name = 'poll/display_result.html'
    model = Choice


    def get_context_data(self, **kwargs):
            context = super(ResultDisplayView, self).get_context_data(**kwargs)
            ques_id = self.kwargs['pk']
            question = get_object_or_404(Question, id=ques_id)
            try:
                selected_choice = question.choice_set.get(id=self.request.GET['choice'])

                context['page']=Question.objects.get(id =ques_id)
                selected_choice.votes += 1
                selected_choice.save()
                return context
            except Exception :
                context['message'] = "no choice selected "
                return context

