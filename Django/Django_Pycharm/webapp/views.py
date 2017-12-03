from django.http import HttpResponse, HttpResponseRedirect


from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms.forms import SignUpForm
from .tokens import account_activation_token

# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User

from webapp.models import Question, Choice
from . import paypal



def index(request):
    reg_user(request)
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
    print('mango')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print("potato")
        if form.is_valid():
            print("salda")
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('webapp/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            print("user")
            return redirect( 'webapp/account_activation_sent.html')
    else:
        print("unot")
        form = SignUpForm()
    return render(request, 'webapp/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('webapp/paytest.html')
    else:
        return render(request, 'webapp/account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'webapp/account_activation_sent.html')

def submitToInvoice(request, groupID):
    results = paypal.submitToInvoice(groupID)
    context = {"results": results}
    return render(request, 'webapp/submitToInvoiceConfirmation.html', context)
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
