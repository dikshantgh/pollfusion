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
    
    
    
    
# from django.http import HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404

# # Create your views here.
# from django.urls import reverse
# from django.utils.datastructures import MultiValueDictKeyError
# from django.views.generic import TemplateView, ListView, DetailView

# from main.models import Question, Choice


# class HomePageView(TemplateView):
#     template_name = 'main/homepage.html'


# class ListPageView(ListView):
#     model = Question
#     template_name = 'main/list_questions.html'


# class DetailPageView(DetailView):
#     model = Question
#     template_name = 'main/detail_questions.html'


# class ResultPageView(DetailView):
#     model = Question
#     template_name = 'main/result.html'

#     # always call POST method if the action is post or GET if the method is GET

#     # def pos(self, request, *args, **kwargs):
#     #     print(self.kwargs)

#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     selected_choice = self.request.GET['radio_choice']
#     #     choice_number = get_object_or_404(Choice, pk=selected_choice)
#     #     choice_number.vote += 1
#     #     choice_number.save()
#     #     return context

#     def dispatch(self, request, *args, **kwargs):
#         # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#         obj = self.get_object()
#         # print('#########################')
#         try:
#             # choice_selected = obj.choices.get(pk=self.request.GET['radio_choice'])
#             choice_selected = get_object_or_404(Choice, pk=self.request.GET['radio_choice'])
#             # print('-------------------')
#         except KeyError:
#             #print('cool', obj.pk)
#             return HttpResponseRedirect(reverse('main:detail_questions', args=[obj.pk, ]))
#         except AttributeError:
#             return HttpResponseRedirect(reverse('main:detail_questions', args=[obj.pk, ]))
#         else:
#             print(choice_selected)
#             choice_selected.vote += 1
#             choice_selected.save()
#             return super().dispatch(request, *args, **kwargs)


# # #
# # def homepage(request):
# #     context = {'name': 'dikshant', 'age': 25}
# #     return render(request, 'main/homepage.html', context)
# #
# #
# # def list_questions(request):
# #     context = {'context': Question.objects.all()}
# #     return render(request, 'main/list_questions.html', context)
# #
# #
# # def detail_questions(request, question_pk):
# #     context = {'context': get_object_or_404(Question, pk=question_pk), }
# #     return render(request, 'main/detail_questions.html', context)
# #
# #
# # def vote_choice(request, question_pk):
# #     context = {'context': get_object_or_404(Question, pk=question_pk), }
# #     try:
# #         obj = get_object_or_404(Choice, pk=request.POST['radio_choice'])
# #         print(request.POST['radio_choice'])
# #
# #     except (KeyError, Choice.DoesNotExist):
# #         context['message'] = "You have not selected any choice"
# #         return render(request, 'main/homepage.html', context)
# #
# #     else:
# #         print(obj)
# #         obj.vote += 1
# #         message = "Your vote is counted successfully"
# #         obj.save()
# #         return HttpResponseRedirect(reverse('main:result', args=[context['context'].pk], ))
# #
# #
# # def result(request, question_pk):
# #     context = {'ques':get_object_or_404(Question, pk= question_pk) }
# #     return render(request, 'main/result.html', context)


 
