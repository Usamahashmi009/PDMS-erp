from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models


from ckeditor_uploader.fields import RichTextUploadingField




# Create your models here.
class Profile(models.Model):

    name = models.CharField(max_length=255)
    mobile1 = models.CharField(max_length=15, blank=True, null=True)
    mobile2 = models.CharField(max_length=15, blank=True, null=True)
    landline = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class AddProperty(models.Model):
    prop_type_choices = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('agricultural', 'Agricultural'),
    ]
    main_property= [
        ('plot', 'Plot'),
        ('house', 'House'),
    ]
    persontype_choices = [
        ('seller', 'Seller'),
        ('purchaser', 'Purchaser'),
    ]
    SIZE_UNIT_CHOICES = [
        ('sqf', 'Square Feet'),
        ('marla', 'Marla'),
        ('kanal', 'Kanal'),
    ]
    size_unit = models.CharField(max_length=10, choices=SIZE_UNIT_CHOICES)
    profile_names = models.ForeignKey(Profile, on_delete=models.CASCADE)
    prop_size = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    price_from = models.DecimalField(max_digits=12, decimal_places=0)
    price_to = models.DecimalField(max_digits=12, decimal_places=0)
    description = models.TextField(blank=True, null=True)
    installment = models.BooleanField(default=False)
    prop_type = models.CharField(max_length=20, choices=prop_type_choices)
    persontype = models.CharField(max_length=20, choices=persontype_choices)
    main_prop = models.CharField(max_length=20, choices=main_property)


    def __str__(self):
        return f"({self.location})"

class crm (models.Model):
    options = [
        ('visited', 'Visited'),
        ('negotiation', 'Negotiation'),
        ('loss', 'Loss'),
    ]

    person_detail = models.ForeignKey(Profile,on_delete=models.CASCADE)
    client_options = models.CharField(max_length=20, choices=options)
    description = models.TextField(blank=True, null=True)
