from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login ,logout
from .forms import UserSingupForm, UserLoginForm,UserUpdateProfileForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from store.models import Transaction
from store.utils import *
from django.db.models import Sum

# Create your views here.

# Start Singup View.

class UserSingupView(View):
    form_class = UserSingupForm
    template_name = 'account/singup.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name, {'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'],cd['email'], cd['password1'])
          
            user = authenticate(request, username = cd['username'], password = cd['password1'])
            login(request,user)
            
            messages.success(request,'Youre account created')
            return redirect('store')
        return render(request,self.template_name,{'form':form})
    
# End Singup View.

# Start Login Viwe

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args ,**kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form =self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['email'], password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'Youre account created')
                return redirect('store')
            messages.error(request,'youre name or pass is wrong try again','warning')
        return render(request,self.template_name,{'form':form})
    
class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'you are logout')
        return redirect('store')
    

class UserProfileView(View):
    def get(self, request, user_id):
        data = cartData(request)
        order = data['order']
        cartItems = data['cartItems']
        user = User.objects.get(id=user_id)
        
        # محاسبه جمع تراکنش‌های کاربر
        
        return render(request, 'account/profile.html', {
            'user': user,
            'cartItems': cartItems,
            'order': order,
              # اضافه کردن total_amount به دیکشنری متغیرهای قالب
        })

    
class UserUpdateProfileView(LoginRequiredMixin, View):
    form_class = UserUpdateProfileForm
    template_name = 'account/upadteprofile.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = User.objects.get(id=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        user = self.user_instance
        if not user.id == request.user.id:
            return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        data = cartData(request)
        cartItems = data['cartItems']
        user = User.objects.get(id=user_id)
        form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form, 'cartItems':cartItems})

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        form = self.form_class(request.POST,  instance=user)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            messages.success(request, 'Your profile has been updated', 'success')
            return redirect('account:user_profile', user.id)
        return render(request, self.template_name, {'form': form})
    


from django.views.generic.list import ListView


class UserTransactions(ListView):
    model = Transaction
    template_name = 'account/transactions.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Transaction.objects.filter(user__id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        
        # محاسبه جمع تراکنش‌های کاربر
        total_amount = Transaction.objects.filter(user__id=user_id).aggregate(total=Sum('amount'))['total']
        
        # دسترسی به سبد خرید و محاسبه تعداد محصولات
        data = cartData(self.request)
        cartItems = data['cartItems']
        
        context['total_amount'] = total_amount  # اضافه کردن total_amount به دیکشنری متغیرهای قالب
        context['cartItems'] = cartItems  # اضافه کردن cartItems به دیکشنری متغیرهای قالب
        return context


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_rest_done')
    email_template_name = 'account/password_reset_email.html'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class PasswordResetConfrimView(auth_views.PasswordResetConfirmView ):
    template_name = 'account/password_reset_confrim.html'
    success_url = reverse_lazy('account:password_reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'