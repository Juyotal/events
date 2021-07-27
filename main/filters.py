import django_filters

from .models import Event, Region


class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains')
    age_limit = django_filters.NumberFilter(lookup_expr='lte')

    location = django_filters.ModelChoiceFilter(
        lookup_expr='isnull', queryset=Region.objects.all())

    class meta:
        model = Event
        fields = ['title', 'location', 'age_limit']
