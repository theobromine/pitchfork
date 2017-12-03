import paypalrestsdk
import random
import string
from paypalrestsdk import Payout, ResourceNotFound


def configure_paypal():
    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": "Af9gJEBMhc_IVgKpynP2C4mpUuqZb3Wtus5bCP3y10EEW-3gFpn89c0aCYgjFvcQBT4MTNuGwXUDUk4S",
        "client_secret": "ED38XvKcXu9iccj4woQqauePZrcC32H4m13ClRnIX-tCzBxsFGTh9sbPi7T8uQoFwV_j93BNh__qqmWG"})


# Create Payment
def create_payment(price):
    configure_paypal()
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:8000/paytest",
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
    else:
        print(payment.error)

    for link in payment.links:
        if link.rel == "approval_url":
            # Convert to str to avoid Google App Engine Unicode issue
            # https://github.com/paypal/rest-api-sdk-python/pull/58
            approval_url = str(link.href)
            return approval_url


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
def create_payout(sender_batch_id, reimbursement_amount, receiver_email, sender_item_i_d):
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
                "sender_item_id": sender_item_i_d
            }
        ]
    })

    if payout.create():
        print("Payout created successfully")
        return True
    else:
        print(payout.error)
        return False


def generate_sender_batch_id():
    return ''.join(random.choice(string.ascii_uppercase) for i in range(12))
            
def submit_to_invoice(groupID): 
    user_contributions = [{"userID": "user1@email.com", "contribution": 3}, {"userID": "user2@email.com", "contribution": 0},{"userID": "user3@email.com", "contribution": 6}]
    #TODO make sure user who will not get a payout and will also not pay in gets an email that says they are all set. 
    total_group_contribution = 0
    for user_contribution in user_contributions:
        total_group_contribution += user_contribution["contribution"]
    cost_per_user = total_group_contribution/len(user_contributions)
    results = {"payouts": 0, "payments": 0, "no_action": 0, "error": 0, "total": len(user_contributions), "cost":cost_per_user}
    for user_contribution in user_contributions:
        if cost_per_user < user_contribution["contribution"]: #User Over contributed. 
            #senderBatchID and groupID are the same thing.
            #receiverEmail and UserId are the same thing. 
            #senderItemID = userID+"-"+groupID.
            create_payout_check = create_payout(groupID, user_contribution["contribution"]-cost_per_user, user_contribution["userID"], user_contribution["userID"]+"-"+groupID)
            if create_payout_check == True:
                results ["payouts"] = results ["payouts"] + 1
            else:
                results ["error"] = results ["error"] + 1
                
        elif cost_per_user > user_contribution["contribution"]:  #User under contributed. 
            create_payment_check = create_payment(cost_per_user-user_contribution["contribution"])
            
            if create_payment_check != None:
                results ["payments"] = results ["payments"] + 1
            else:
                results ["error"] = results ["error"] + 1
                
        else: #cost_per_user = user_contribution[contribution]  #User contributed the perfect ammount. 
            #You are good email
            results ["no_action"] = results ["no_action"] + 1
    return results
