from django.db import models

# Create your models here.

class Review(models.Model):
    billboard=models.ForeignKey('billboard.BillBoard',on_delete=models.CASCADE)
    user=models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    text=models.TextField(max_length=800)
    datetime=models.DateTimeField(auto_now=True)
    rating=models.IntegerField(default=0)