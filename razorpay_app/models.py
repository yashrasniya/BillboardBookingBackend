from django.db import models

# from Home.models import *
# import razorpay
#
# client = razorpay.Client(auth=("rzp_test_vlK7qms1BtJdXt", "GmrIdfs0XYoLWtXsY2E7D5pk"))


# Create your models here.

class Create_payment_link(models.Model):
    choice = [('0', 'Paid'), ('1', 'Pending'), ('-1', 'Failed')]
    user = models.ForeignKey('accounts.User', blank=True, null=True, db_constraint=False, on_delete=models.CASCADE)
    billboard=models.ForeignKey('billboard.BillBoard',on_delete=models.CASCADE)
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


class razorpay_gateway_detail(models.Model):
    razorpay_id = models.CharField(blank=False, null=False, max_length=50)
    razorpay_SECRET = models.CharField(blank=False, null=False, max_length=50)
    call_back_url = models.URLField(blank=False, null=False)




