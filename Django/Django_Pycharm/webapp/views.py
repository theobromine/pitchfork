from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import login, authenticate
from .forms.forms import SignUpForm, ItemForm
from .tokens import account_activation_token

# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from webapp.models import GroupAdmin, Item
from . import paypal


def index(request, message):
    return reg_user(request)
    # return render(request, 'webapp/index.html', {'form': SignUpForm, 'message'} )


def faq(request):
    return render(request, 'webapp/faq.html')


def info(request):
    return render(request, 'webapp/info.html')


def contact(request):
    return render(request, 'webapp/contact.html')


def paytest(request):
    message = ""
    if request.method == "POST":
        payment_amount = request.POST.get('paymentAmount', "")
        receiver_email = request.POST.get('receiverEmail', "")
        reimbursement_amount = request.POST.get('reimbursementAmount', "")
        if payment_amount != "":
            paypal_id = paypal.create_payment(payment_amount, request.build_absolute_uri())
            approval_url = paypal.get_payment_url(paypal_id)
            return redirect(approval_url)
        else:
            sender_batch_id = paypal.generate_sender_batch_id()
            sender_item_id = "1"
            if paypal.create_payout(sender_batch_id, reimbursement_amount, receiver_email, sender_item_id):
                message = "Your payout has been Successfully executed."
            else:
                message = "Unfortunately, your payout was unsucessful."
    payer_id = request.GET.get("PayerID", "")
    payment_id = request.GET.get("paymentId", "")

    if payer_id != "":
        if paypal.execute_payment(payer_id, payment_id):
            message = "Your payment has been Successfully executed."
        else:
            message = "Unfortunately, your payment was unsucessful."
    context = {"message": message}
    return render(request, 'webapp/paytest.html', context)


def reg_user(request):
    print('mango')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print("potato")
        if form.is_valid():
            print("salda")
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            # current_site = get_current_site(request)
            # user.email_user(subject, message)
            print("user")
            message = "Success!"
            return render(request, 'webapp/index.html', {'form': form, 'message': message})
    else:
        form = SignUpForm()
        message = ''
    return render(request, 'webapp/index.html', {'form': form, 'message': message})


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
        return render(request, 'webapp/account/account_activation_email.html')


def account_activation_sent(request):
    return render(request, 'webapp/account/account_activation_sent.html')


def user_home(request):
    return render(request, 'webapp/userhome.html')


def group_home(request, group_id):
    user_id = request.user.id

    try:
        group_admin = GroupAdmin.objects.get(group_id=group_id, user_id=user_id)
    except ValueError:
        group_admin = None

    if group_admin is not None:
        is_admin = True
    else:
        is_admin = False

    is_admin = is_admin | request.user.is_staff
    status = paypal.get_group_payment_statuses(user_id, group_id)
    items = Item.objects.filter(group_id=group_id)
    context = {"group_id": group_id, "is_admin": is_admin,
               "status": status, "items": items}  # checks if they are an admin and displays only if they are.
    return render(request, 'webapp/grouphome.html', context)


def new_group(request):
    return render(request, 'webapp/newgroup.html')


def settings(request):
    return render(request, 'webapp/settings.html')


def invoice_confirmation(request, group_id):
    user_id = request.user.id

    try:
        group_admin = GroupAdmin.objects.get(group_id=group_id, user_id=user_id)
    except:
        group_admin = None

    if group_admin is not None:
        is_admin = True
    else:
        is_admin = False

    is_admin = is_admin | request.user.is_staff
    status = paypal.get_group_payment_statuses(user_id, group_id)

    if (is_admin is not True) or (status["all_confirmed"] is not True) or (status["group_invoiced_date"] is not None):
        return redirect("../grouphome/" + str(group_id))

    results = paypal.invoice_confirmation(group_id, request.build_absolute_uri("/paypal_return"))
    context = {"results": results, "group_id": group_id}
    return render(request, 'webapp/invoice_confirmation.html', context)


def paypal_return(request):
    payment_id = request.GET.get("paymentId", "")
    payer_id = request.GET.get("PayerID", "")
    group_id = paypal.paypal_return(payment_id, payer_id)
    return redirect("./grouphome/" + str(group_id))


def add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, "./grouphome/" + str(group_id), {
        'form': ItemForm()
    })


@login_required
def test(request):
    return render(request, 'webapp/test.html')

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
