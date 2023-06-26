from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.core.paginator import Paginator


from django.core.paginator import Paginator

from django.core.paginator import Paginator

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    
    paginator = Paginator(products, 3)  # تعداد محصولات در هر صفحه
    
    page_number = request.GET.get('page')
    page_list = paginator.get_page(page_number)
    
    context = {
        'products': page_list,
        'cartItems': cartItems,
        'page_list': page_list,  # اضافه کردن page_list به context
    }
    
    return render(request, 'store/store.html', context)

def detail(request, product_id):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    product = Product.objects.get(id=product_id)
    tags = Tag.objects.all().filter(products=product)

   

    context = {
        'product': product,
        'cartItems': cartItems,
        'items': items,
        'order': order,
        'tags': tags,
    }
    return render(request, 'store/detail.html', context)

def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total():
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    # Save transaction
    for item in order.orderitem_set.all():
        transaction = Transaction.objects.create(
            user=customer.user,
            product=item.product,
            amount=item.get_total(),
        )
        transaction.save()

    return JsonResponse('Payment submitted..', safe=False)

def Search(request):
    search = request.GET.get('search')
    product_list = Product.objects.filter(name__iexact=search)
    return render(request, 'store/product_list.html', {'product_list': product_list})