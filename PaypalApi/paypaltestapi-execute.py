import paypalrestsdk
paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AbRQ7t6DHN-58-pu8Y9Jpyec7zzK7yp-3IH0E-YD9hylHtAt7_zp6U6Seu5dmYamdtWt082jCbMhdzgo",
  "client_secret": "EHmaYDd2IsfEgzvMutyMaB2ZMe4HV_NAiF8XnyEtij7JTIg29RASZ9m9GtmR8uBzTi9aqY54X5cU7MCt" })
  
payment = paypalrestsdk.Payment.find("PAY-0GM87810SR049963LLIAR34Y")

if payment.execute({"payer_id": "DJM97ZMN8UPKG"}):
  print("Payment execute successfully")
else:
  print(payment.error) # Error Hash