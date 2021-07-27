from django.db.models import query
from django.db.models.query import QuerySet
from django.views.generic.detail import DetailView

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, Guest
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, request
from django.views.generic.list import ListView
from accounts.models import Profile
from .filters import EventFilter
from .forms import DiscountForm, EventForm
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.


# class EventCreate(LoginRequiredMixin, CreateView):
#     model = Event
#     fields = '__all__'
#     template_name = 'main/event_add.html'
#     success_url = reverse_lazy('main:events')

#     def form_valid(self, form):
#         form.instance.user = self.request.user

#         return super(EventCreate, self).form_valid(form)


def eventcreate(request):

    context = {}

    form = EventForm(request.POST)

    form_2 = DiscountForm(request.POST)

    if form.is_valid():
        event = form.save()

    if form_2.is_valid():
        discount = form_2.save()
        discount.event = event
        discount.save()

        return redirect('main:events')

    context['form'] = form
    context['form_2'] = form_2
    return render(request, "main/event_add.html", context)


# class EventDelete(DeleteView):
#     model = Event
#     context_object_name = 'event'
#     success_url = reverse_lazy('main:events')


def eventdelete(request, event_id):

    context = {}

    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":

        event.delete()
        return redirect("main:events")

    return render(request, "main/eventdelete.html", context)


@login_required
def book(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if (event.seats > 0):
        try:
            Guest.objects.create(user=request.user, group=event)

        except IntegrityError:
            messages.warning(request, ("Warning, already a member of event"))

        else:
            messages.success(request, ("You are now a member of the event"))
            event.seats -= 1
            event.save()
        return redirect('main:detail', event_id)
    else:
        messages.info(request, "sorry! the event is fully booked!")
        return redirect('main:detail', event_id)


@login_required
def unbook(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    try:
        guest = Guest.objects.filter(
            user=request.user,
            group=event
        ).get()
    except Guest.DoesNotExist:
        messages.warning(
            request,
            "You can't unbook because you aren't booked."
        )
    else:
        event.seats += 1
        guest.delete()
        event.save()

        messages.success(request, "You have successfully unbooked.")

    return redirect('main:detail', event_id)


# class EventsView(ListView):

#     model = Event
#     template_name = 'main/events_list.html'
#     context_object_name = 'events'

#     def get_context_data(self, **kwargs):
#         # # myfilter = EventFilter()
#         # context = super().get_context_data(**kwargs)
#         # # context['tasks'] = context['tasks'].filter(user=self.request.user)
#         # context['myfilter'] = EventFilter(
#         #     self.request.GET, queryset=self.get_queryset())
# #         return context

def eventsview(request):

    if request.user.is_authenticated:
        profile = request.user.profile
    else:
        profile = None

    events = Event.objects.all()

    age = int(request.GET.get('age_limit')) if request.GET.get(
        'age_limit') else None

    if profile and age and profile.age >= age:
        events = events.filter(age_limit__lt=profile.age)

    filter = EventFilter(request.GET, queryset=events)

    return render(request, 'main/events_list.html', {'events': filter})


# class EventDetail(DetailView):
#     model = Event
#     template_name = 'main/event_detail.html'
#     context_object_name = 'event'

def eventdetail(request, event_id):
    context = {}
    event = Event.objects.get(pk=event_id)
    context["event"] = event
    # if event.discount:
    #     context['discount'] = event.discount

    return render(request, "main/event_detail.html", context)


def discountaction(request, event_id):
    event = Event.objects.get(pk=event_id)
    discount = event.discount if event.discount else None
    age = discount.discount_age if discount.discount_age else None

    if request.user.is_authenticated:
        profile = request.user.profile
    else:
        profile = None

    if profile and age and profile.age >= age:
        event.price = (event.price * (100 - discount.discount))//100
        event.save()
        return redirect('main:detail', event_id)

    else:
        messages.info(request, "sorry! you do not qualify for the discount")
        return redirect('main:detail', event_id)


# def filterthisbaby(request):
#     context = {}
#     qs = Event.objects.all()

#     title_query = request.GET.get('title_contains')

#     age_min = request.GET.get('age_min')

#     if title_query != '' and title_query is not None:
#         qs = qs.filter(title__contains=title_query)

#     if age_min != '' and age_min is not None:
#         qs = qs.filter(age_limit__gte=age_min)

#     context['qs'] = qs

#     return render(request, "main/events_list.html", context)
