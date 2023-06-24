from django.shortcuts import render
from django.views import View
from store.models import *
from django.views.generic import ListView
# Create your views here.


class CategoryView(View):
    def get(self, request, product_slug):
        product = Product.objects.filter(category__slug = product_slug)
        return render(request, 'group/product_list.html', {'product':product})
    



class ProductListByTypeView(ListView):
    model = Product
    template_name = 'product_list.html'

    def get_queryset(self):
        product_type = self.kwargs['product_type']
        queryset = Product.objects.filter(type=product_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_type = self.kwargs['product_type']
        categories = Category.objects.filter(products__type=product_type).distinct()
        context['categories'] = categories
        return context