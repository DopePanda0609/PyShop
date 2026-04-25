from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import Address

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to log in.')
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'accounts/orders.html', {'orders': user_orders})

@login_required
def addresses(request):
    user_addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    return render(request, 'accounts/addresses.html', {'addresses': user_addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        
        Address.objects.create(
            user=request.user,
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            is_default=not Address.objects.filter(user=request.user).exists()
        )
        messages.success(request, 'Address added successfully!')
        return redirect('accounts:addresses')
        
    return render(request, 'accounts/add_address.html')
