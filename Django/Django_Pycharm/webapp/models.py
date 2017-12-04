import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email_confirmed = models.BooleanField(default=False)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Item(models.Model):
    # Item Name
    name = models.CharField(max_length=50, blank=False)
    # Item Price
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # Who is bringing the item.
    pitched = models.ForeignKey(User, on_delete=models.CASCADE)
    # A link to a picture of the item
    picture = models.CharField(max_length=200, blank=True)
    # Has the item been confirmed by the admin?
    confirmed = models.BooleanField(default=False)


#
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    # GroupId     = models.ForeignKey(Question, on_delete=models.CASCADE)
    group_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    paid_bit = models.BooleanField(default=False)
    paypal_id = models.CharField(max_length=50)
    paid_date = models.DateTimeField(null=True)


class Payout(models.Model):
    payout_id = models.AutoField(primary_key=True)
    # GroupId     = models.ForeignKey(Question, on_delete=models.CASCADE)
    group_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    paid_bit = models.BooleanField(default=False)
    paypal_id = models.CharField(max_length=50)
    paid_date = models.DateTimeField(null=True)
