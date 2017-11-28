from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from webapp.models import Question, Choice


def index(request):
    return render(request, 'webapp/index.html')


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'webapp/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'webapp/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'webapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('webapp:results', args=(question.id,)))


def reg_user(request):
    context = {}
    print("test")
    if request.POST:
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        email = request.POST["email"]
        passwd = request.POST["passwd"]
        return render(request, 'webapp/index.html', context)
    return render(request, 'webapp/index.html')


def faq(request):
    return render(request, 'webapp/faq.html')


def info(request):
    return render(request, 'webapp/info.html')


def contact(request):
    return render(request, 'webapp/contact.html')


def paytest(request):
    return render(request, 'webapp/paytest.html')
