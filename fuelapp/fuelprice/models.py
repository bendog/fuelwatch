from typing import List
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property

# Create your models here.


class Feature(models.Model):
    name = models.CharField(_("Feature"), max_length=50, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    brand = models.CharField(_("Brand"), max_length=50)
    trading_name = models.CharField(_("Trading Name"), max_length=150, null=True)
    phone = models.CharField(_("Phone"), max_length=50, null=True)
    address = models.CharField(_("Address"), max_length=250)
    suburb = models.CharField(_("Location"), max_length=80)
    latitude = models.FloatField(_("Latitude"))
    longitude = models.FloatField(_("Longitude"))
    # site_features = models.CharField(_("Site Features"), max_length=250, null=True)
    features = models.ManyToManyField(Feature, verbose_name=_("Features"))

    class Meta:
        unique_together = ['brand', 'address', 'suburb']

    def __str__(self):
        return f"Location:{self.pk}: {self.brand} {self.suburb}"

    @cached_property
    def feature_list(self) -> List[str]:
        return [x.name for x in self.features.all()]

    @cached_property
    def name(self):
        return f"{self.brand} {self.suburb}"

class Price(models.Model):
    date = models.DateField(_("Date"), auto_now=False, auto_now_add=False)
    price = models.FloatField(_("Price"))
    location = models.ForeignKey(Location, verbose_name=_("Location"), on_delete=models.CASCADE, related_name='prices')

    def __str__(self):
        return f"{self.date} {self.location} - {self.price}"
