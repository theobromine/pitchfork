from django.http import HttpResponse, HttpResponseRedirect


from django.contrib.auth import login, authenticate
from .forms.forms import SignUpForm

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from webapp.models import Question, Choice
from . import paypal

def index(request):
    return render(request, 'webapp/index.html', {'form': SignUpForm})


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


def faq(request):
    return render(request, 'webapp/faq.html')

def info(request):
    return render(request, 'webapp/info.html')

def contact(request):
    return render(request, 'webapp/contact.html')

def paytest(request):
    message = ""
    if request.method=="POST":
        paymentAmount = request.POST.get('paymentAmount', "")
        receiverEmail = request.POST.get('receiverEmail', "")
        reimbursementAmount = request.POST.get('reimbursementAmount', "")
        if paymentAmount != "":
            approval_url = paypal.createPayment(paymentAmount)
            return redirect(approval_url)
        else:
            senderBatchID = paypal.generateSenderBatchID()
            senderItemID = "1"
            if paypal.createPayout(senderBatchID, reimbursementAmount, receiverEmail, senderItemID):
                message = "Your payout has been Successfully executed."
            else:
                message = "Unfortunately, your payout was unsucessful." 
    payerID = request.GET.get("PayerID","")
    paymentID = request.GET.get("paymentId","")
    
    if payerID != "":
        if paypal.executePayment(payerID, paymentID): 
            message = "Your payment has been Successfully executed."
        else:
            message = "Unfortunately, your payment was unsucessful." 
    context={"message":message}
    return render(request, 'webapp/paytest.html', context)
    
def paytestReturn(request):
    payerID = request.GET['payerID']
    paymentID = request.GET['paymentID']
    executePayment(payerID, paymentID)
    return render(request, 'webapp/paytest.html')


def reg_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'webapp/signup.html', {'form': form})

#
# def reg_user(request):
#     context = {}
#     form = UserCreationForm()
#
#     print("test")
#     if request.POST:
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('passwd')
#
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             # return redirect('home')
#             return render(request, 'webapp/index.html', context)
#
#         # firstname = request.POST["first_name"]
#         # lastname = request.POST["last_name"]
#         # email = request.POST["email"]
#         # passwd = request.POST["passwd"]
#
#     else:
#         form = UserCreationForm()
#     # return render(request, 'signup.html', {'form': form})
#     #     return render(request, 'webapp/index.html', context)
#     return render(request, 'webapp/index.html', {'form': form})
#     # return render(request, 'webapp/index.html')
