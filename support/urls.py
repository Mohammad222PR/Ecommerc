from django.urls import path
from . import views


urlpatterns = [ 
    path('ticket/<int:user_id>/',views.TicketView.as_view(), name='ticket_user'),
    path('ticket/detail/<int:t_id>/', views.DetailTicket.as_view(), name = 'detail_ticket'),
    path('ticket/add/',views.AddTicketView.as_view(), name = 'add_ticket'),
    path('add_answer/<int:t_id>/',views.AddTicketAnswerView.as_view(), name='add_answer'),
]