from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Choice

# Create your views here.


def index(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'questions': questions})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id, pub_date__lte=timezone.now())
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = Question.objects.get(pk=question_id)
    selected_choice = question.choices.get(pk=request.POST['choice'])
    selected_choice.vote()
    return redirect('polls:results', question_id=question_id)
