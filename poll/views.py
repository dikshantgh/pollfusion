from django.shortcuts import render,HttpResponse
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from poll.models import QuestionType, Question, Choice, Contact
from django.core.urlresolvers import reverse_lazy
from poll.forms import QuestionTypeForm, QuestionForm, ChoiceForm, ContactForm
from django.shortcuts import get_object_or_404, render
from django.db.models import Max, Sum
# Create your views here.


class QuestionTypeView(ListView):

    # lists all question type
    model = QuestionType
    template_name = "poll/main_page.html"
    context_object_name ="type_list"

    
    def get_popular(self):

        political = QuestionType.objects.get(topic = "Political")
        maxx = Question.objects.all().exclude(question_type=political).aggregate(Max('hit_ques'))
        return Question.objects.get(hit_ques = int(maxx['hit_ques__max']))

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['popular'] = self.get_popular()
        return context   


        
class QuestionBriefView(ListView):

    model = Question
    template_name = "poll/question_list.html"


    def get_queryset(self,**kwargs):
        topic_name = get_object_or_404(QuestionType, id=self.kwargs['pk'])
        return Question.objects.filter(question_type=topic_name)
    
    def get_data(self):
        topic_name = get_object_or_404(QuestionType, id=self.kwargs['pk'])
        ques = Question.objects.filter(question_type__topic=topic_name).count()
        return ques
        

    def get_context_data(self, **kwargs):
       
        context = super(QuestionBriefView, self).get_context_data(**kwargs)
        context['typeid']=self.kwargs['pk']
        context['show']=self.get_data()
        return context



class QuestionDetailView(DetailView):

    model = Question
    template_name = "poll/question_detail.html"


    def get_total (self):

        query = self.object.choice_set.all()        
        total = query.aggregate(Sum('votes'))
        return total['votes__sum']

    def get_data(self, **kwargs):
        ques_id = self.kwargs['pk']
        page =  Question.objects.get(id =ques_id)
        page.hit_ques = page.hit_ques + 1
        page.save()

        return page.hit_ques

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['view']= self.get_data()
        context['total']=self.get_total()
        return context
   
    

class TypeCreateView(CreateView):


    form_class = QuestionTypeForm
    template_name = "poll/create_type.html"
    success_url = reverse_lazy('poll:main_page')



class QuestionCreateView(CreateView):


    form_class = QuestionForm
    template_name = "poll/create_question.html"

    def get_initial(self):

        initials = super(QuestionCreateView, self).get_initial()
        initials['question_type'] = self.kwargs['pk']
        return initials

    def get_success_url(self,**kwargs):
        
        post = self.object.question_type # it prints out the clicked question type or the new created question
        #print(self.object.id) # printts the id of question
        return reverse_lazy('poll:question_list', args = (post.id,))

        

class OptionCreateView(CreateView):


    form_class = ChoiceForm
    template_name = "poll/create_option.html"

    def get_initial(self):
        initials = super(OptionCreateView, self).get_initial()
        initials['question'] = self.kwargs['pk']
        return initials

    def get_success_url(self,**kwargs):

        post = self.object.question 
        return reverse_lazy('poll:question_detail', args = (post.id,))
    
    
    
class QuestionUpdateView(UpdateView):

    model = Question
    template_name = "poll/create_question.html"
    form_class = QuestionForm

    def get_success_url(self,**kwargs):

        post = self.object.question_type # it prints out the clicked question type or the new created question
        #print(self.object.id) # printts the id of question
        return reverse_lazy('poll:question_list', args = (post.id,))



class QuestionDeleteView(DeleteView):

    model = Question
    template_name = "poll/delete_question.html"


    def get_success_url(self,**kwargs):

        post = self.object.question_type # it prints out the clicked question type or the new created question
        #self.soft_delete()
        return reverse_lazy('poll:question_list', args = (post.id,))



class OptionDeleteView(DeleteView):

    model = Choice
    template_name = "poll/delete_option.html"
    #alive = True

    #def __init__(self,**kwargs):
    # Bulk delete bypasses individual objects' delete methods.
       # Choice.objects.get(id =self.kwargs['pk']).delete(alive=False)
     #   print(self.object.question)

    def get_success_url(self,**kwargs):
        post = self.object.question
        print(post)
        pp=(self.object.id)
        Choice.objects.get(id =pp).delete(alive=False)
        return reverse_lazy('poll:question_detail', args = (post.id,))




class OptionUpdateView(UpdateView):

    model = Choice
    template_name = "poll/create_option.html"
    form_class = ChoiceForm

    def get_success_url(self,**kwargs):

        post = self.object.question 
        return reverse_lazy('poll:question_detail', args = (post.id,))



class ResultDisplayView(DetailView):            # to display the final results

    template_name = 'poll/display_result.html'
    model = Choice

    def get_data (self, **kwargs):
        
        ques_id = self.kwargs['pk']
        question = get_object_or_404(Question, id=ques_id)
        return question

    def get_context_data(self, **kwargs):
            print(self.object)
            context = super(ResultDisplayView, self).get_context_data(**kwargs)
            question = self.get_data() 
            context['page']=question

            try:
                selected_choice = question.choice_set.get(id=self.request.GET["choice"])
                selected_choice.votes += 1
                selected_choice.save()
                                  
            except Exception as ex :
                context['message']="not selected "+str(ex)
                
            return context



class TypeDeleteView(DeleteView):

    model = QuestionType
    template_name = "poll/delete_type.html"

    def get_success_url(self,**kwargs):
        
        post = self.object.topic
        return reverse_lazy('poll:main_page')



class ContactAddView(CreateView):

    
    model = Contact
    template_name = "poll/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('poll:contact_views')

    def form_valid(self, form):
        self.request.session['name'] = form.cleaned_data
        self.request.session['address'] = form.cleaned_data
        return super(ContactAddView, self).form_valid(form)

class ResultView(TemplateView):
    template_name = "contact.html"

 