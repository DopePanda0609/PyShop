from django.shortcuts import render
from django.db.models import Q
from .models import Product


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def new(request):
    from django.http import HttpResponse
    return HttpResponse('new products')


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})


def search(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query)
        )

    if category:
        products = products.filter(category=category)

    # Determine the page title
    if category:
        category_labels = {
            'vegetables-fruits': 'Vegetables & Fruits',
            'dairy-bread': 'Dairy & Bread',
            'snacks-drinks': 'Snacks & Drinks',
            'meat-fish': 'Meat & Fish',
            'cleaning': 'Cleaning',
            'bath-body': 'Bath & Body',
            'paper-goods': 'Paper Goods',
            'pet-care': 'Pet Care',
        }
        page_title = category_labels.get(category, category.replace('-', ' ').title())
    elif query:
        page_title = f'Results for "{query}"'
    else:
        page_title = 'All Products'

    return render(request, 'search.html', {
        'products': products,
        'query': query,
        'category': category,
        'page_title': page_title,
    })


def address(request):
    saved_address = request.session.get('delivery_address', '')
    if request.method == 'POST':
        addr = request.POST.get('address', '').strip()
        if addr:
            request.session['delivery_address'] = addr
            return render(request, 'address.html', {
                'saved_address': addr,
                'success': True,
            })
    return render(request, 'address.html', {'saved_address': saved_address})