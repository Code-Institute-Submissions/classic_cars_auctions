import django_filters
from .models import Car


class CarFilter(django_filters.FilterSet):
    """Filter class"""
    make = django_filters.CharFilter(lookup_expr='icontains')

    year_gt = django_filters.NumberFilter(field_name='firstRegistred',
                                          lookup_expr='gt')
    year_lt = django_filters.NumberFilter(field_name='firstRegistred',
                                          lookup_expr='lt')

    reserved_price_gt = django_filters.NumberFilter(field_name='reservedPrice',
                                                    lookup_expr='gt')
    reserved_price_lt = django_filters.NumberFilter(field_name='reservedPrice',
                                                    lookup_expr='lt')

    fuel_type = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        """Filter Meta class"""
        model = Car
        fields = ['make', 'firstRegistred', 'fuelType', 'reservedPrice']
