#MVC (Model - Model; View - Template; Controller - View)
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from student.models import Student

class StudentList(ListView):
    model = Student

class StudentCreate(CreateView):#Контроллер-класс производный от класса CreateView из модуля django.views.generic.edit.
    model = Student
    fields = ['name','section','age', 'course', 'mail', 'website']
    success_url = reverse_lazy('student:student_list') #возврат URL-адреса как переменной по умолчанию для параметров функции

class StudentUpdate(UpdateView):
    model = Student
    fields = ['name','section','age', 'course', 'mail', 'website']
    success_url = reverse_lazy('student:student_list')

class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('student:student_list')
'''
def question_detail(request, question_id):#Контроллер-функция 
    try:
        q = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'quiz/question_detail.html', {question_id: q})
'''