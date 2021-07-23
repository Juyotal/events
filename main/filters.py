import django_filters

from .models import Event


class EventFilter(django_filters.FilterSet):
    class meta:
        model = Event
        fields = ('title', 'location', 'booked')
