import razorpay
# client = razorpay.Client(auth=("rzp_test_vlK7qms1BtJdXt", "GmrIdfs0XYoLWtXsY2E7D5pk"))
client = razorpay.Client(auth=("rzp_live_M02QbtfQJlQ4O8", "pxcGYJTKy2rc2fSIoLTlvrJA"))
print(client)
o=client.payment_link.create({
  "amount": 500,
  "currency": "INR",
  "accept_partial": True,
  "first_min_partial_amount": 100,
  "description": "For XYZ purpose",
  "customer": {
    "name": "Gaurav Kumar",
    "email": "gaurav.kumar@example.com",
    "contact": "+919999999999"
  },
  "notify": {
    "sms": False,
    "email": False
  },
  "reminder_enable": True,
  "notes": {
    "policy_name": "Jeevan Bima"
  },
  "callback_url": "https://example-callback-url.com/",
  "callback_method": "get"
})

print(o)