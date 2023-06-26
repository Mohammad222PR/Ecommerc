from django.contrib import admin
from .models import Ticket, TicketAnswer

class TicketAnswerInline(admin.StackedInline):
    model = TicketAnswer
    extra = 0

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'complete']
    list_filter = ['complete']
    search_fields = ['title', 'user__username']
    inlines = [TicketAnswerInline]