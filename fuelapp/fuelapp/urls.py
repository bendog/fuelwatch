"""fuelapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from graphene_django.views import GraphQLView
from fuelprice import views as fuelprice_views

router = routers.DefaultRouter()
router.register(r'feature', fuelprice_views.FeatureViewSet)
router.register(r'location', fuelprice_views.LocationViewSet)
router.register(r'price', fuelprice_views.PriceViewSet)

urlpatterns = [
    path('update/', fuelprice_views.import_data),
    path('admin/', admin.site.urls),
    path('rest/', include(router.urls)),
    path('graphql', GraphQLView.as_view(graphiql=True)),
    path('list/', fuelprice_views.list_prices),
]
