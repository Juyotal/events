from django.urls import path
from .views import eventdetail, eventsview, book, unbook, eventcreate, eventdelete, discountaction


app_name = 'main'

urlpatterns = [

    # path('', index, name='index'),
    path('', eventsview, name='events'),
    path('book/<int:event_id>/', book, name='book'),
    path('discount/<int:event_id>/', discountaction, name='discount'),
    path('event_add/', eventcreate, name='eventadd'),
    path('event_delete/<int:event_id>/', eventdelete, name='eventdelete'),
    path('<int:event_id>/', eventdetail, name='detail'),
    path('unbook/<int:event_id>/', unbook, name='unbook'),


]
