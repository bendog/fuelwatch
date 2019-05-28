from django.contrib import admin
from .models import Feature, Location, Price

# Register your models here.
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass
