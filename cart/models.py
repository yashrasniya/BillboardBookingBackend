from django.db import models

# Create your models here.

class CartItem(models.Model):
    user=models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    billboard=models.ForeignKey('billboard.BillBoard',on_delete=models.CASCADE)
    datetime=models.DateTimeField(null=True,blank=True)