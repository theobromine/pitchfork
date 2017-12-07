from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class GroupAdmin(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_group(self):
        return self.group


class Item(models.Model):
    # Item Name
    name = models.CharField(max_length=50, blank=False)
    # Item Price
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # Who is bringing the item.
    pitched = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # A link to a picture of the item
    picture = models.ImageField(upload_to='item/%Y/%m/%d', null=True, blank=True)
    # Has the item been confirmed by the admin?
    confirmed = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    paid_bit = models.BooleanField(default=False)
    paypal_id = models.CharField(max_length=50)
    paid_date = models.DateTimeField(null=True)


class Payout(models.Model):
    payout_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    paid_bit = models.BooleanField(default=False)
    paypal_id = models.CharField(max_length=50)
    paid_date = models.DateTimeField(null=True)


class UserContribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    username = models.TextField()
    contribution = models.DecimalField(max_digits=5, decimal_places=2)
    email = models.TextField()


class Meta:
    managed = False
