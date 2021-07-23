from django.db.models import query
from django.db.models.query import QuerySet
from django.views.generic.detail import DetailView

from django.core.checks import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, Guest
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.list import ListView
from accounts.models import Profile
from .filters import EventFilter


# Create your views here.


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = '__all__'
    template_name = 'main/event_add.html'
    success_url = reverse_lazy('main:events')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(EventCreate, self).form_valid(form)


class EventDelete(DeleteView):
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('main:events')


@login_required
def book(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if (event.booked is False):

        # Guest.objects.create(user=request.user, event=event)
        event.seats -= 1
        event.booked = True
        event.save()
        return redirect('main:detail', event_id)


class EventsView(ListView):
    model = Event
    template_name = 'main/events_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        # myfilter = EventFilter()
        context = super().get_context_data(**kwargs)
        context['myfilter'] = EventFilter(
            self.request.GET, queryset=self.get_queryset())
        return context

# def eventsview(request):
#     events = Event.objects.all()

#     myFilter = EventFilter(request.GET, queryset=events)

#     context = {'events': events, 'myfilter': myFilter}

#     return render(request, 'main/events_list.html', context)


class EventDetail(DetailView):
    model = Event
    template_name = 'main/event_detail.html'
    context_object_name = 'event'
