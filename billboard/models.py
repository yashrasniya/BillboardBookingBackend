import razorpay
from django.db import models
import django
from razorpay import Payment

from accounts.models import User
from razorpay_app.models import Create_payment_link, razorpay_gateway_detail

try:
    RGD = razorpay_gateway_detail.objects.all()[0]
    # client = razorpay.Client(auth=("rzp_test_u01RD7HTlF1ysu", "oJclH13vmmj5evdT5HeKXrOG"))pxcGYJTKy2rc2fSIoLTlvrJA
    client = razorpay.Client(auth=(RGD.razorpay_id, RGD.razorpay_SECRET))
except (django.db.utils.ProgrammingError, razorpay_gateway_detail.DoesNotExist, django.db.utils.OperationalError,
        IndexError) as e:
    RGD=razorpay_gateway_detail.objects.create(razorpay_id='',razorpay_SECRET='',call_back_url='')
    print(e)
# Create your models here.

class BillBoard(models.Model):
    # address

    address = models.ForeignKey('Address', on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=10)
    location_type = models.ForeignKey('LocationType', on_delete=models.CASCADE)
    banner_type = models.ForeignKey('BannerType', on_delete=models.CASCADE)

    description = models.TextField(max_length=20000)

    def __str__(self):
        return self.size + ' ' + str(self.address)


class Address(models.Model):
    country = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    landmark = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.address} {self.landmark} {self.city} {self.country}"


class BannerType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LocationType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Images(models.Model):
    img = models.FileField(upload_to='BillBoard/Image')
    billboard = models.ForeignKey(BillBoard, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.billboard) + ' ' + self.img.url


class bookingHistory(models.Model):
    billboard = models.ForeignKey(BillBoard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    payment=models.ForeignKey(Create_payment_link, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bookingHistory/')


    def fetching_link(self,callBackUrl=RGD.call_back_url):
        user_contact = self.user.mobile_number
        # price ############################
        # price ############################
        price=int(((self.end_date-self.start_date).days/30)*int(self.billboard.price))
        # price ############################
        # price ############################
        try:
            int(user_contact)
        except ValueError as e:
            user_contact = '9888888888'

        p = client.payment_link.create({
            "amount": price*100,
            "currency": "INR",

            "reference_id": f'NINE{self.payment.id}',
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
        self.payment.short_url = p['short_url']
        self.payment.save()
        return {'link': p['short_url']}





    def createingPaymentLink(self,**kwargs):
        callBackUrl=kwargs.get('callBackUrl',RGD.call_back_url)
        price=((self.end_date-self.start_date).days/30)*int(self.billboard.price)
        self.payment = Create_payment_link.objects.create(amount=str(price),
                                                 user=self.user,
                                                 billboard=self.billboard,
                                                 callBackUrl=callBackUrl
                                                 )
    def save(self,*args,**kwargs):
        self.createingPaymentLink(**kwargs)

        super(bookingHistory,self).save(*args,**kwargs)


