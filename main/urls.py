from django.urls import path
from .views import EventCreate, EventDelete, EventDetail, EventsView, book


app_name = 'main'

urlpatterns = [

    # path('', index, name='index'),
    path('', EventsView.as_view(), name='events'),
    path('book/<int:event_id>/', book, name='book'),
    path('event_add/', EventCreate.as_view(), name='eventadd'),
    path('<int:pk>/', EventDetail.as_view(), name='detail'),


]
