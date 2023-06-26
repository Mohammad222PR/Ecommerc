from django.urls import path
from . import views


urlpatterns = [ 
    path('ticket/<int:user_id>',views.TicketView.as_view(), name='ticket_user'),
    path('ticket/detail/<int:t_id>/', views.DetailTicket.as_view(), name = 'detail_ticket'),
    path('ticket/add/',views.AddTicketView.as_view(), name = 'add_ticket'),
    path('support/ticket/update/<int:t_id>/', views.TicketUpdateView.as_view(), name='update_ticket'),
    path('ticket/delete/<int:t_id>/',views.DeleteTicketView.as_view(), name='delete_ticket'),
]