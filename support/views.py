from django.shortcuts import render, redirect
from django.views import View
from .forms import TicketandupdateForm
from .models import *
from store.models import *
from store.utils import *
from django.contrib import messages

# Create your views here.



class TicketView(View):
    template_name = 'support/ticket.html'

    def get(self, request,user_id):
        data = cartData(request)
        cartItems = data['cartItems']

        tickets = Ticket.objects.filter(user_id=user_id) 

        context = {
            'tickets': tickets,
            'cartItems': cartItems,
        }
        return render(request, self.template_name, context)

class DetailTicket(View):
    def get(self, request, t_id):
        data = cartData(request)
        cartItems = data['cartItems']
        ticket = Ticket.objects.get(id=t_id)
        answers = ticket.ticketanswer_set.filter(ticket=ticket)  
        context = {
            'ticket': ticket,
            'answers': answers,
            'cartItems':cartItems
        }
        return render(request, 'support/detail.html', context)
class AddTicketView(View):
    form_class = TicketandupdateForm
    tempalte_name = 'support/ticket_add.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('store')
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request):
        data = cartData(request)
        cartItems = data['cartItems']
        form = self.form_class()

        context = {
            'form': form,
            'cartItems': cartItems
        }
        return render(request, self.tempalte_name, context)


    def post(self, request):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            new_t = form.save(commit=False)
            new_t.user = request.user
            new_t.body = form.cleaned_data['body']
            new_t.save()
            return redirect('ticket_user', user.id)
        
        context = {
            'form': form
        }
        return render(request, self.tempalte_name, context)


class TicketUpdateView(View):
    form_class = TicketandupdateForm
    template_name = 'support/update.html'

    def setup(self, request, *args, **kwargs):
        self.ticket_instance = Ticket.objects.get(id = kwargs['t_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('store')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, t_id):
        
        ticket = self.ticket_instance
        ticket = Ticket.objects.get(id = t_id)
        form = self.form_class(instance=ticket)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, t_id):
        user = request.user 
        ticket = self.ticket_instance
        ticket = Ticket.objects.get(id = t_id)
        form = self.form_class(request.POST, instance = ticket)
        if form.is_valid():
            form.save()
            messages.success(request,'Youre profile updatd','success')
            return redirect('ticket_user',user.id)
        
    

class DeleteTicketView(View):
    def get(self, request, t_id):
        user = request.user
        ticket = Ticket.objects.get(id = t_id)
        if ticket.user.id == request.user.id:
            ticket.delete()
            messages.success(request,'Yore Ticket Delete!','success')
            return redirect('ticket_user', user.id)