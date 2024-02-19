from django.db import models
from django.utils.timezone import localtime, timedelta
from django.urls import reverse
from secrets import token_urlsafe


# Create your models here.



class Customer(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



class ResetPassword(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    used = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        self.token = self.token or token_urlsafe(50)
        return super().save(*args, **kwargs)

    def is_valid(self):
        not_used = not self.used
        not_expired = (localtime() - timedelta(days=1)) < self.created
        return not_used and not_expired
    
    def get_absolute_url(self):
        return reverse("reset_password", kwargs={"token": self.token})