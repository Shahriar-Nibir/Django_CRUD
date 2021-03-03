from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .filters import *
from .decorators import *

# Create your views here.


@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #group = None
            # if request.user.groups.exists():
            #    group = request.user.groups.all()[0].name
            # if group == 'admin':
            return redirect('home')
            # else:
            #    return redirect('user')
        else:
            messages.info(request, "Incorrect Credentials")
    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user)
            messages.info(request, "User created " + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)


@login_required(login_url='login')
# @allowed_user(allowed_role=['admin'])
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = Order.objects.filter(status="Delivered").count()
    pending = Order.objects.filter(status="Pending").count()
    context = {'customers': customers, 'orders': orders, 'total': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    total_orders = orders.count()
    context = {'customer': customer, 'orders': orders,
               'total': total_orders, 'myFilter': myFilter}
    return render(request, 'customer.html', context)


@login_required(login_url='login')
def product(request):
    products = Product.objects.filter()
    return render(request, 'product.html', {'products': products})


@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    formset = OrderFormSet(instance=customer)
    context = {'customer': customer, 'form': formset}
    if request.method == 'POST':
        form_set = OrderFormSet(request.POST, instance=customer)
        if form_set.is_valid:
            customer = form_set.cleaned_data[1]
            product = form_set.cleaned_data[1]
            status = form_set.cleaned_data[1]
            form_set.save()
            return redirect('/')
    return render(request, 'create_order.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    context = {'form': form}
    if request.method == 'POST':
        f = OrderForm(request.POST, instance=order)
        if f.is_valid:
            f.save()
            return redirect('/')
    return render(request, 'create_order.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
def delete(request, pk):
    order = Order.objects.get(id=pk)
    context = {'order': order}
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    return render(request, 'delete.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['customer'])
def user(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {'orders': orders, 'total': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'userPage.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['customer'])
def userSettings(request):
    customer = request.user.customer
    forms = CustomerForm(instance=customer)
    if request.method == 'POST':
        f = CustomerForm(request.POST, request.FILES, instance=customer)
        if f.is_valid:
            f.save()
    context = {'forms': forms}
    return render(request, 'userSettings.html', context)
