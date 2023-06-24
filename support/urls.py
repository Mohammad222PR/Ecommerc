from django.urls import path
from . import views


urlpatterns = [ 
    path('ticket/',views.TicketView.as_view(), name='ticket_user')
    path('ticket/detail/<int:t_id>', views.DetailTicket.as_view(), name = 'detail_ticket')
]