from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from rest_framework import viewsets

from .models import Price, Location, Feature
from .serializers import FeatureSerializer, LocationSerializer, PriceSerializer

FUEL_WATCH_RSS_URL = "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS"


def get_fuel_file() -> str:
    """ return a string of the rss feed xml """
    with open("/Users/ben.fitz/dev/fuelwatch/rss.xml") as fo:
        content = fo.read()
    content = content.replace('trading-name', 'trading_name')
    content = content.replace('site-features', 'site_features')
    return content


def get_fuel_feed() -> str:
    """ return a string of the rss feed xml """
    with urlopen(FUEL_WATCH_RSS_URL) as fp:
        content = fp.read().decode()
    content = content.replace('trading-name', 'trading_name')
    content = content.replace('site-features', 'site_features')
    return content


def import_data(request):
    content = get_fuel_feed()
    soup = BeautifulSoup(content, 'xml')
    price_added = 0
    location_added = 0
    for item in soup.rss.channel.find_all('item'):
        # setup site features
        site_features = []
        if item.site_features:
            site_features = [x.strip() for x in item.site_features.string.split(',') if x.strip()]

        # setup fuel locations
        fuel_location = {
            "brand": item.brand.string,
            "suburb": item.location.string,
            "address": item.address.string,
            "phone": item.phone.string,
            "latitude": item.latitude.string,
            "longitude": item.longitude.string,
            "trading_name": item.trading_name.string,
        }
        fl, fl_created = Location.objects.get_or_create(**fuel_location)
        if fl_created:
            location_added += 1
            feature_pks = []
            for feature_name in site_features:
                feat, feat_created = Feature.objects.get_or_create(name=feature_name)
                feature_pks.append(feat.pk)
            if feature_pks:
                fl.features.set(list(set(feature_pks)))
                fl.save()

        # process fuel price
        fuel_price = {
            "date": item.date.string,
            "price": float(item.price.string),
            "location": fl,
        }
        fp, created = Price.objects.get_or_create(
            **fuel_price
        )
        if created:
            price_added += 1
        print(fp)
    response = HttpResponse(f"added_locations:{location_added}\nadded_prices:{price_added}", content_type="text/plain")
    if location_added or price_added:
        response.status_code = 201
    return response


# django rest viewsets

class PriceViewSet(viewsets.ModelViewSet):
    serializer_class = PriceSerializer
    queryset = Price.objects.select_related('location').all()
    search_fields = (
        'location__suburb',
        'location__brand',
        'price',
    )
    filter_fields = {
        'price': ['gt', 'gte', 'lt', 'lte'],
        'date': ['gt', 'gte', 'lt', 'lte'],
        'location__brand': ['icontains', 'istartswith', 'in'],
        'location__suburb': ['icontains', 'istartswith', 'in'],
    }


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.prefetch_related('features', 'prices').all()
    search_fields = ('suburb', 'brand')
    filter_fields = {
        'prices__price': ['gt', 'gte', 'lt', 'lte'],
        'prices__date': ['gt', 'gte', 'lt', 'lte'],
        'brand': ['icontains', 'istartswith', 'in'],
        'suburb': ['icontains', 'istartswith', 'in'],
    }


class FeatureViewSet(viewsets.ModelViewSet):
    serializer_class = FeatureSerializer
    queryset = Feature.objects.filter(name__isnull=False)
