import paypalrestsdk
from paypalrestsdk import Payout, ResourceNotFound

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "Af9gJEBMhc_IVgKpynP2C4mpUuqZb3Wtus5bCP3y10EEW-3gFpn89c0aCYgjFvcQBT4MTNuGwXUDUk4S",
  "client_secret": "ED38XvKcXu9iccj4woQqauePZrcC32H4m13ClRnIX-tCzBxsFGTh9sbPi7T8uQoFwV_j93BNh__qqmWG" })
  
payout = Payout({
    "sender_batch_header": {
        "sender_batch_id": "1234567",
        "email_subject": "You have a payment"
    },
    "items": [
        {
            "recipient_type": "EMAIL",
            "amount": {
                "value": 0.99,
                "currency": "USD"
            },
            "receiver": "shirt-supplier-one@mail.com",
            "note": "Thank you.",
            "sender_item_id": "item_1"
        }
    ]
})

if payout.create():
  print("Payout created successfully")
else:
  print(payout.error)