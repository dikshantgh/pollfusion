from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from poll.models import QuestionType, Question, Choice
from django.core.urlresolvers import reverse_lazy
from poll.forms import QuestionTypeForm, QuestionForm, ChoiceForm

# Create your views here.


class QuestionTypeView(ListView):


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


    
    
