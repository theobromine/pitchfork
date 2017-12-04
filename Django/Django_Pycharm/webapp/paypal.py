import paypalrestsdk
import random
import string
import datetime
from webapp.models import Payout as models_payout
from webapp.models import Payment as models_payment
from paypalrestsdk import Payment, Payout, ResourceNotFound


def configure_paypal():
    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": "Af9gJEBMhc_IVgKpynP2C4mpUuqZb3Wtus5bCP3y10EEW-3gFpn89c0aCYgjFvcQBT4MTNuGwXUDUk4S",
        "client_secret": "ED38XvKcXu9iccj4woQqauePZrcC32H4m13ClRnIX-tCzBxsFGTh9sbPi7T8uQoFwV_j93BNh__qqmWG"})


# Create Payment
def create_payment(price, is_test):
    if is_test:
        return_url = "http://localhost:8000/paytest"
    else:
        return_url = "http://localhost:8000/paypal_return"

    configure_paypal()
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": "http://localhost:8000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "pitchforkContribution",
                    "sku": "item",
                    "price": price,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": price,
                "currency": "USD"},
            "description": "This is your contribution to your groups total bill."}]})

    if payment.create():
        print("Payment created successfully")
        return payment.id
    else:
        print(payment.error)
        return None


def get_payment_url(paypal_id):
    configure_paypal()
    payment = Payment.find(paypal_id)
    print(paypal_id)
    for link in payment.links:
        if link.rel == "approval_url":
            # Convert to str to avoid Google App Engine Unicode issue
            # https://github.com/paypal/rest-api-sdk-python/pull/58
            approval_url = str(link.href)
            return approval_url
    return None


def get_payment_url_from_user_and_group(user_id, group_id):
    try:
        payment = models_payment.objects.get(user_id=user_id, group_id=group_id)
        return get_payment_url(payment.paypal_id)
    except:
        return None


# Execute Payment
def execute_payment(payer_id, payment_id):
    configure_paypal()

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        print("Payment execute successfully")
        return True
    else:
        print(payment.error)  # Error Hash
        return False


# Create Payout
def create_payout(sender_batch_id, reimbursement_amount, receiver_email, sender_item_id):
    configure_paypal()
    payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": sender_batch_id,
            "email_subject": "You have a payment"
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": reimbursement_amount,
                    "currency": "USD"
                },
                "receiver": receiver_email,
                "note": "Thank you.",
                "sender_item_id": sender_item_id
            }
        ]
    })

    if payout.create():
        print("Payout created successfully")
        return payout.batch_header.payout_batch_id
    else:
        print(payout.error)
        return None


def generate_sender_batch_id():
    return ''.join(random.choice(string.ascii_uppercase) for i in range(12))


def invoice_confirmation(group_id):
    # TODO Sample Data, delete after database is set up, Currently hard coded.
    user_contributions = [{"user_id": "user1@email.com", "contribution": 3},
                          {"user_id": "user2@email.com", "contribution": 0},
                          {"user_id": "user3@email.com", "contribution": 6}]
    total_group_contribution = 0
    for user_contribution in user_contributions:
        total_group_contribution += user_contribution["contribution"]
    cost_per_user = total_group_contribution / len(user_contributions)
    results = {"payouts": 0, "payments": 0, "no_action": 0, "error": 0, "total": len(user_contributions),
               "cost": cost_per_user, "user_contributions": user_contributions,
               "total_group_contribution": total_group_contribution}
    index = 0
    for user_contribution in user_contributions:
        index = index + 1
        user_contribution["difference"] = user_contribution["contribution"] - cost_per_user
        user_contribution["difference_non_neg"] = cost_per_user - user_contribution["contribution"]
        if cost_per_user < user_contribution["contribution"]:  # User Over contributed, payout.
            # senderBatchID and group_id are the same thing.
            # receiverEmail and user_id are the same thing.
            # senderItemID = user_id+"-"+group_id.

            payout_id = create_payout(group_id, user_contribution["contribution"] - cost_per_user,
                                      user_contribution["user_id"],
                                      user_contribution["user_id"] + "-" + group_id)
            if payout_id is not None:
                results["payouts"] = results["payouts"] + 1
                payout = models_payout(group_id=group_id, user_id=index, amount=user_contribution["difference"],
                                       # TODO change back to user_contribution["user_id"], Hard set
                                       paid_bit=True, paypal_id=payout_id, paid_date=datetime.datetime.now())
                payout.save()
            else:
                results["error"] = results["error"] + 1

        elif cost_per_user > user_contribution["contribution"]:  # User under contributed, payment.
            payment_id = create_payment(cost_per_user - user_contribution["contribution"], False)

            if payment_id != None:
                results["payments"] = results["payments"] + 1
                payment = models_payment(group_id=group_id, user_id=index,
                                         amount=user_contribution["difference_non_neg"],
                                         # TODO change back to user_contribution["user_id"], Hard set
                                         paid_bit=False, paypal_id=payment_id, paid_date=None)
                payment.save()
            else:
                results["error"] = results["error"] + 1

        else:  # cost_per_user = user_contribution[contribution]  #User contributed the perfect ammount.
            # TODO You are good email/ webpage
            results["no_action"] = results["no_action"] + 1
    return results


def paypal_return(payment_id, payer_id):
    payment = models_payment.objects.get(paypal_id=payment_id)
    group_id = payment.group_id
    if execute_payment(payer_id, payment_id):
        print("The payment has been Successfully executed.")
        payment.paid_bit = True
        payment.paid_date = datetime.datetime.now()
        payment.save()
    else:
        print("Unfortunately, the payment was unsucessful.")
    return group_id


def get_group_payment_statuses(user_id, group_id):
    paypal_url = None
    paypal_url = get_payment_url_from_user_and_group(user_id, group_id)
    reimbursement_date = None
    reimbursement_amount = None
    payment_amount = None
    payment_date = None
    group_payouts = models_payout.objects.filter(group_id=group_id)

    if group_payouts.count() > 0:
        group_invoiced_date = group_payouts[0].paid_date
    else:
        group_invoiced_date = None

    try:
        payout_object = models_payout.objects.get(group_id=group_id, user_id=user_id)
        reimbursement_date = payout_object.paid_date
        reimbursement_amount = payout_object.amount
    except:
        payout_object = None

    try:
        payment_object = models_payment.objects.get(group_id=group_id, user_id=user_id)
        payment_date = payment_object.paid_date
        payment_amount = payment_object.amount
    except:
        payout_object = None

    status = {"paypal_url": paypal_url, "reimbursement_date": reimbursement_date,
              "reimbursement_amount": reimbursement_amount, "payment_amount": payment_amount,
              "payment_date": payment_date, "group_invoiced_date": group_invoiced_date}

    return status
