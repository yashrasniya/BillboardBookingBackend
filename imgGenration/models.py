from django.db import models


# Create your models here.

class openAiConfig(models.Model):
    api_key = models.CharField(max_length=400)
    server_on = models.BooleanField(default=False)
    model_name=models.CharField(max_length=20)
    img_size=models.CharField(max_length=20)


class generationsHistory(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    img_url = models.URLField(max_length=2000)
    img = models.ImageField(upload_to='generations',blank=True,null=True)
    text = models.TextField(max_length=5000)
