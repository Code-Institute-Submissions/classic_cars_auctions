import django_filters
from .models import Car


class CarFilter(django_filters.FilterSet):
    """Filter class"""
    make = django_filters.CharFilter(field_name='make',
                                     lookup_expr='icontains')

    year_gt = django_filters.NumberFilter(field_name='firstRegistred',
                                          lookup_expr='gte') 
    year_lt = django_filters.NumberFilter(field_name='firstRegistred',
                                          lookup_expr='lte')

    reserved_price_gt = django_filters.NumberFilter(field_name='reservedPrice',
                                                    lookup_expr='gte')
    reserved_price_lt = django_filters.NumberFilter(field_name='reservedPrice',
                                                    lookup_expr='lte')

    fuel_type = django_filters.CharFilter(field_name='fuelType',
                                          lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description',
                                            lookup_expr='icontains')

    class Meta:
        """Filter Meta class"""
        model = Car
        fields = ['make', 'firstRegistred', 'fuelType', 'reservedPrice']
