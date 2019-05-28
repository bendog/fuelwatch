from rest_framework import serializers
from .models import Feature, Location, Price


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('name',)


class SimplePriceSerializer(serializers.ModelSerializer):
    """ simple price serializer, without nested location """

    class Meta:
        model = Price
        fields = ('id', 'date', 'price')


class SimpleLocationSerializer(serializers.ModelSerializer):
    """ simple location serializer without nested price """

    class Meta:
        model = Location
        fields = (
            'id', 'brand', 'trading_name', 'phone', 'address', 'suburb',
            'latitude', 'longitude', 'feature_list'
        )


class LocationSerializer(serializers.ModelSerializer):
    """ complex location serializer with nested values """
    prices = SimplePriceSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = (
            'id', 'brand', 'trading_name', 'phone', 'address', 'suburb',
            'latitude', 'longitude', 'feature_list', 'prices'
        )


class PriceSerializer(serializers.ModelSerializer):
    """ complex price serializer with nested values """
    location = SimpleLocationSerializer(read_only=True)

    class Meta:
        model = Price
        fields = '__all__'
