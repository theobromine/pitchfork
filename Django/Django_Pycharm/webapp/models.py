import datetime
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
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Test(models.Model):
    test = models.CharField(max_length=20)

class Item(models.Model):
    # Item Name
    name        = models.CharField(max_length=50, blank=False)
    # Item Price
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    # Who is bringing the item.
    pitched     = models.ForeignKey(User, on_delete=models.CASCADE)
    # A link to a picture of the item
    picture     = models.CharField(max_length=200, blank=True)
    # Has the item been confirmed by the admin?
    confirmed   = models.BooleanField(default=False)




# use `WebSys`
# # Migrated from PaypalAPI docs
#
# class PitforkPayments(models.Model):
#     PaymentId   = models.AutoField(primary_key=True)
#     GroupId     = models.ForeignKey(Question, on_delete=models.CASCADE)
#     UserId      =  int NOT NULL,
#     Amount      = decimal(5,2) NOT NULL,
#     Paidbit     = models.IntegerField(default=, max_length=1)
#     PaypalId    = varchar(50) NULL,
#     PaidDate    = datetime NULL,
#   PRIMARY KEY (PaymentId)
# );
#
# CREATE TABLE IF NOT EXISTS `pitchfork_payouts` (
#   PayoutId int NOT NULL auto_increment,
#   GroupId int NOT NULL,
#   UserId int NOT NULL,
#   Amount decimal(5,2) NOT NULL,
#   Paid bit NOT NULL,
#   PaypalId varchar(50) NULL,
#   PaidDate datetime NULL,
#   PRIMARY KEY PayoutId
# );