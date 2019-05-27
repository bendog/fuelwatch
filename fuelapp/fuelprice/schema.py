import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter

from .models import Feature, Location, Price

class FeatureType(DjangoObjectType):

    class Meta:
        model = Feature
        interfaces = (graphene.Node, )
        filter_fields = ['name']

class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        interfaces = (graphene.Node, )
        filter_fields = ['brand', 'suburb']

class PriceFilter(FilterSet):
    order_by = OrderingFilter(
        fields=(
            ('date', 'date')
        )
    )
    class Meta:
        model = Price
        exclude = []
    

class PriceType(DjangoObjectType):
    class Meta:
        model = Price
        interfaces = (graphene.Node, )
        filter_fields = ['date', 'price', 'location']

class Query(object):
    feature = graphene.Node.Field(FeatureType)
    all_features = DjangoFilterConnectionField(FeatureType)
    location = graphene.Node.Field(LocationType)
    all_locations = DjangoFilterConnectionField(LocationType)
    price = graphene.Node.Field(PriceType)
    all_prices = DjangoFilterConnectionField(PriceType, filterset_class=PriceFilter)

    # def resolve_all_features(self, info, **kwargs):
    #     return Feature.objects.all()

    # def resolve_all_locations(self, info, **kwargs):
    #     return Location.objects.select_related('features').all()

    # def resolve_all_prices(self, info, **kwargs):
    #     return Price.objects.select_related('location').all()
