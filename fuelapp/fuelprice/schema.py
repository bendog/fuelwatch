import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter

from .models import Feature, Location, Price


# FILTER SETS


class LocationFilter(FilterSet):
    order_by = OrderingFilter(
        fields=(
            ('suburb', 'suburb'),
            ('brand', 'brand'),
            ('prices__price', 'prices__price'),
        )
    )

    class Meta:
        model = Location
        exclude = []
        fields = {
            # 'prices__price': ['gt', 'gte', 'lt', 'lte'],
            # 'prices__date': ['gt', 'gte', 'lt', 'lte'],
            'brand': ['exact', 'icontains', 'istartswith', 'in'],
            'suburb': ['exact', 'icontains', 'istartswith', 'in'],
        }


class PriceFilter(FilterSet):
    order_by = OrderingFilter(
        fields=(
            ('date', 'date'),
            ('price', 'price'),
        )
    )

    class Meta:
        model = Price
        exclude = []
        fields = {
            'price': ['gt', 'gte', 'lt', 'lte'],
            'date': ['gt', 'gte', 'lt', 'lte'],
            # 'location__brand': ['exact', 'icontains', 'istartswith', 'in'],
            # 'location__suburb': ['exact', 'icontains', 'istartswith', 'in'],
        }


# NODES


class FeatureType(DjangoObjectType):

    class Meta:
        model = Feature
        interfaces = (graphene.relay.Node, )
        filter_fields = ['name']


class LocationType(DjangoObjectType):
    prices = DjangoFilterConnectionField("fuelprice.schema.PriceType", filterset_class=PriceFilter)

    class Meta:
        model = Location
        interfaces = (graphene.relay.Node, )

    def resolve_prices(self, info, **kwargs):
        return PriceFilter(kwargs).qs.filter(location=self.pk)


class PriceType(DjangoObjectType):
    class Meta:
        model = Price
        interfaces = (graphene.relay.Node, )


# QUERY


class Query(object):
    feature = graphene.relay.Node.Field(FeatureType)
    all_features = DjangoFilterConnectionField(FeatureType)

    location = graphene.relay.Node.Field(LocationType, filterset_class=LocationFilter)
    all_locations = DjangoFilterConnectionField(LocationType, filterset_class=LocationFilter)

    price = graphene.relay.Node.Field(PriceType, filterset_class=PriceFilter)
    all_prices = DjangoFilterConnectionField(PriceType, filterset_class=PriceFilter)

    # def resolve_all_features(self, info, **kwargs):
    #     return Feature.objects.all()

    # def resolve_all_locations(self, info, **kwargs):
    #     return Location.objects.select_related('features').all()

    # def resolve_all_prices(self, info, **kwargs):
    #     return Price.objects.select_related('location').all()
