from django.shortcuts import render, redirect
from django.views import View
from .forms import TicketForm
from .models import *
# Create your views here.



class AllTicket(View):
    template_name = 'support/ticket.html'
    def get(self, request):
        ticket = Ticket.objects.filter(user = request.user)

        context = {
            'ticket':ticket,
        }
        return render(request,self.template_name, context)




class DetailTicketView(View):
    def get(self, request, t_id):
        tikcet = Ticket.objects.get(id = t_id)


class TicketView(View):
    form_class = TicketForm
    tempalte_name = 'support/ticket.html'
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
            return redirect('')
