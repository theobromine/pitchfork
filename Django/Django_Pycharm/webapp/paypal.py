import paypalrestsdk
import random
import string
from paypalrestsdk import Payout, ResourceNotFound


def configurePaypal():
    paypalrestsdk.configure({
    "mode": "sandbox", # sandbox or live
    "client_id": "Af9gJEBMhc_IVgKpynP2C4mpUuqZb3Wtus5bCP3y10EEW-3gFpn89c0aCYgjFvcQBT4MTNuGwXUDUk4S",
    "client_secret": "ED38XvKcXu9iccj4woQqauePZrcC32H4m13ClRnIX-tCzBxsFGTh9sbPi7T8uQoFwV_j93BNh__qqmWG" })

#Create Payment
def createPayment(price):
    configurePaypal()
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
    
#Execute Payment
def executePayment(payerID, paymentID):
    configurePaypal()
     
    payment = paypalrestsdk.Payment.find(paymentID)
    
    if payment.execute({"payer_id": payerID}):
        print("Payment execute successfully")
        return True
    else:
        print(payment.error) # Error Hash
        return False

#Create Payout
def createPayout(senderBatchID, reimbursementAmount, receiverEmail, senderItemID):
    configurePaypal()
    payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": senderBatchID,
            "email_subject": "You have a payment"
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": reimbursementAmount,
                    "currency": "USD"
                },
                "receiver": receiverEmail,
                "note": "Thank you.",
                "sender_item_id": senderItemID
            }
        ]
    })
    
    if payout.create():
        print("Payout created successfully")
        return True
    else:
        print(payout.error)
        return False
        
def generateSenderBatchID():
    return ''.join(random.choice(string.ascii_uppercase) for i in range(12))
    
def submitToInvoice(groupID): 
    userContributions = [{"userID": "user1@email.com", "contribution": 3}, {"userID": "user2@email.com", "contribution": 0},{"userID": "user3@email.com", "contribution": 6}]
    #TODO make sure user who will not get a payout and will also not pay in gets an email that says they are all set. 
    totalGroupContribution = 0
    for userContribution in userContributions:
        totalGroupContribution += userContribution["contribution"]
    costPerUser = totalGroupContribution/len(userContributions)
    results = {"Payouts": 0, "Payments": 0, "noAction": 0, "error": 0, "total": len(userContributions), "cost":costPerUser}
    for userContribution in userContributions:
        if costPerUser < userContribution["contribution"]: #User Over contributed. 
            #senderBatchID and groupID are the same thing.
            #receiverEmail and UserId are the same thing. 
            #senderItemID = userID+"-"+groupID.
            createPayoutCheck = createPayout(groupID, userContribution["contribution"]-costPerUser, userContribution["userID"], userContribution["userID"]+"-"+groupID)
            if createPayoutCheck == True:
                results ["Payouts"] = results ["Payouts"] + 1
            else:
                results ["error"] = results ["error"] + 1
                
        elif costPerUser > userContribution["contribution"]:  #User under contributed. 
            createPaymentCheck = createPayment(costPerUser-userContribution["contribution"])
            
            if createPaymentCheck != None:
                results ["Payments"] = results ["Payments"] + 1
            else:
                results ["error"] = results ["error"] + 1
                
        else: #costPerUser = userContribution[contribution]  #User contributed the perfect ammount. 
            #You are good email
            results ["noAction"] = results ["noAction"] + 1
    return results
