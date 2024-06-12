from django.db import models

import razorpay
from django.db import models
import django
from razorpay import Payment

from accounts.models import User


# Create your models here.

class Create_payment_link(models.Model):
    choice = [('0', 'Paid'), ('1', 'Pending'), ('-1', 'Failed')]
    user = models.ForeignKey('accounts.User', blank=True, null=True, db_constraint=False, on_delete=models.CASCADE)
    billboard=models.ManyToManyField('billboard.BillBoard')
    status = models.CharField(choices=choice, default='Pending', max_length=32)
    amount = models.DecimalField(max_digits=10, blank=False, null=False,decimal_places=2)
    short_url = models.URLField(blank=False, null=False)
    payment_link_id = models.CharField(blank=False, null=False, max_length=32)
    payment_link_status = models.CharField(blank=False, null=False, max_length=32)
    razorpay_payment_id = models.CharField(blank=False, null=False, max_length=32)
    reference_id = models.CharField(blank=False, null=False, max_length=32)
    callBackUrl = models.URLField(blank=False, null=False, max_length=1000)

    razorpay_signature = models.CharField(blank=False, null=False, max_length=320)
    date_time=models.DateTimeField(auto_now_add=True)

    def fetching_link(self,price,callBackUrl=callBackUrl):
        RGD = razorpay_gateway_detail.objects.all()[0]
        try:

            client = razorpay.Client(auth=(RGD.razorpay_id, RGD.razorpay_SECRET))
        except Exception as e:
            print(e)
            raise e
        user_contact = self.user.mobile_number
        # price ############################
        # price ############################
        # price=int(((self.end_date-self.start_date).days/30)*int(self.billboard.price))
        # price ############################
        # price ############################
        try:
            int(user_contact)
        except ValueError as e:
            user_contact = '9888888888'

        p = client.payment_link.create({
            "amount": int(price*100),
            "currency": "INR",

            "reference_id": f'NINE0{self.id}',
            "callback_url": callBackUrl,
            "description": "Payment for policy no #23456",
            "customer": {
                "name": self.user.username,
                "contact": user_contact,
                "email": self.user.email
            },
            "notify": {
                "sms": False,
                "email": False
            },
            "reminder_enable": True,
            "options": {
                "checkout": {
                    "theme": {
                        "hide_topbar": True
                    }
                }
            }
        })
        print(p['short_url'])
        self.short_url = p['short_url']
        self.save()
        return {'link': p['short_url']}


class razorpay_gateway_detail(models.Model):
    razorpay_id = models.CharField(blank=False, null=False, max_length=50)
    razorpay_SECRET = models.CharField(blank=False, null=False, max_length=50)
    call_back_url = models.URLField(blank=False, null=False)




