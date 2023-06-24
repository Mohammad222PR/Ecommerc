from django.shortcuts import render, redirect
from django.views import View
from .forms import TicketForm, TicketAnswerForm
from .models import *
# Create your views here.



class TicketView(View):
    template_name = 'support/ticket.html'
    def get(self, request):
        ticket = Ticket.objects.filter(user = request.user)

        context = {
            'ticket':ticket,
        }
        return render(request,self.template_name, context)


class DetailTicket(View):
    def get(self, request, t_id):
        ticket = Ticket.objects.get(id=t_id)
        answers = ticket.ticketanswer_set.filter(ticket=ticket)  
        context = {
            'ticket': ticket,
            'answers': answers
        }
        return render(request, 'support/detail.html', context)
class AddTicketView(View):
    form_class = TicketForm
    tempalte_name = 'support/ticket_add.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()

        context = {
            'form':form,
        }
        return render(request,self.tempalte_name, context)


    def post(self, request):
        form = self.form_class(request.POST,  request.FIELS)
        if form.is_valid():
            new_t = form.save(commit = False)
            new_t.user = request.user
            new_t.body = form.cleaned_data['body']
            new_t.save()
        if 'images' in form.cleaned_data:
            new_t.images = form.cleaned_data['images']
            new_t.save()
            return redirect('detail.html', new_t.id)
        
        context = {
            'form':form
        }
        return render(request,self.tempalte_name, context)
    

class AddTicketAnswerView(View):
    form_class = TicketAnswerForm
    template_name = 'support/answer_add.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, t_id):
        ticket = Ticket.objects.get(id = t_id)
        form = self.form_class(instance=ticket)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, t_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.ticket = Ticket.objects.get(id=t_id)
            new_answer.name = request.user
            new_answer.body = form.cleaned_data['body']
            new_answer.save()

            # Update ticket complete status to True
            ticket = new_answer.ticket
            ticket.complete = True
            ticket.save()

            return redirect('detail_ticket', t_id)

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)