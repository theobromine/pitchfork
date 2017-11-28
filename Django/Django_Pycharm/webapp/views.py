from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf.urls import url, include
#for paypalintegration only
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.pdt.views import process_pdt
from webapp.models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    print("test")
    context = {'latest_question_list': latest_question_list}
    ctx = {}
    print("test")
    if request.POST:
        ctx['rlt'] = request.POST["first_name"]
        return render(request, 'webapp/index.html', ctx)

    return render(request, 'webapp/index.html', context)


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
    ctx = {}
    print("test")
    if request.POST:
        ctx['rlt'] = request.POST['q']
        ctx['rlt'] = request.POST["first_name"]
    return render(request, 'webapp/index.html', ctx)

def faq(request):
    return render(request, 'webapp/faq.html')

def info(requst):
    return render(request, 'webapp/info.html')

def contact(request):
    return render(request, 'webapp/contact.html')

#http://django-paypal.readthedocs.io/en/stable/standard/ipn.html
def paytest(request):
    print("test")

    # What you want the button to do.
    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "10000000.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        ##below is broken as hell
        #we need to have a proper url here.
        "notify_url": request.build_absolute_uri(reverse('faq')),
        "return_url": request.build_absolute_uri(reverse(contact(request))),
        "cancel_return": request.build_absolute_uri(reverse(faq(request))),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "paytest.html", context)


# @require_GET
def payment(request):
    pdt_obj, failed = process_pdt(request)
    context = {"failed": failed, "pdt_obj": pdt_obj}
    if not failed:

        # WARNING!
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)

        if pdt_obj.receiver_email == "receiver_email@example.com":

            # ALSO: for the same reason, you need to check the amount
            # received etc. are all what you expect.

            # Do whatever action is needed, then:
            return render(request, 'my_valid_payment_template', context)
    return render(request, 'my_non_valid_payment_template', context)
#
# def show_me_the_money(sender, **kwargs):
#     ipn_obj = sender
#     if ipn_obj.payment_status == ST_PP_COMPLETED:
#         # WARNING !
#         # Check that the receiver email is the same we previously
#         # set on the `business` field. (The user could tamper with
#         # that fields on the payment form before it goes to PayPal)
#         if ipn_obj.receiver_email != "receiver_email@example.com":
#             # Not a valid payment
#             return
#
#         # ALSO: for the same reason, you need to check the amount
#         # received, `custom` etc. are all what you expect or what
#         # is allowed.
#
#         # Undertake some action depending upon `ipn_obj`.
#         if ipn_obj.custom == "premium_plan":
#             price = ...
#         else:
#             price = ...
#
#         if ipn_obj.mc_gross == price and ipn.mc_currency == 'USD':
#             ...
#     else:
#         #...
#
