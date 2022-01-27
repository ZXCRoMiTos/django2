import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from mainapp.models import Product, ProductCategory
from django.views.generic import View


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_product_price(request, pk):
    if is_ajax(request=request):
        product = Product.objects.filter(pk=pk).first()
        return JsonResponse(
            {'price': product and product.price or 0}
        )


def get_hot_product():
    product_ids = Product.objects.values_list('id', flat=True).all()
    random_id = random.choice(product_ids)
    return Product.objects.get(pk=random_id)


def get_popular_products():
    return Product.objects.all().order_by('-views')[:4]


def get_new_products():
    return Product.objects.all().order_by('-created')[:4]


def same_products(hot_product):
    return Product.objects.filter(category=hot_product.category). \
               exclude(pk=hot_product.pk)[:3]


class Index(View):
    def get(self, request):
        context = {'page_title': 'главная',
                   'top_products': get_popular_products(),
                   'new_products': get_new_products(), }
        return render(request, 'mainapp/index.html', context)


class Products(View):
    def get(self, request):
        hot_product = get_hot_product()
        context = {'page_title': 'каталог',
                   'hot_product': hot_product,
                   'same_products': same_products(hot_product), }
        return render(request, 'mainapp/products.html', context)


class Category(View):
    def get(self, request, pk):
        page_num = request.GET.get('page', 1)
        if pk == 0:
            category = {'pk': 0, 'name': 'все'}
            products = Product.objects.all()
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = category.product_set.all()

        products_paginator = Paginator(products, 2)
        try:
            products = products_paginator.page(page_num)
        except PageNotAnInteger:
            products = products_paginator.page(1)
        except EmptyPage:
            products = products_paginator.page(products_paginator.num_pages)

        context = {
            'page_title': 'товары категории',
            'category': category,
            'products': products,
        }
        return render(request, 'mainapp/category_products.html', context)


class ProductPage(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.views += 1
        product.save()
        context = {
            'page_title': 'страница продукта',
            'product': product,
        }
        return render(request, 'mainapp/product_page.html', context)


class Contact(View):
    def get(self, request):
        locations = [
            {'city': 'Москва',
             'phone': '+7-888-444-7777',
             'email': 'info@geekshop.ru',
             'address': 'В пределах МКАД'},
            {'city': 'Санкт-Петербург',
             'phone': '+7-888-333-9999',
             'email': 'info.spb@geekshop.ru',
             'address': 'В пределах КАД'},
            {'city': 'Хабаровск',
             'phone': '+7-888-222-3333',
             'email': 'info.east@geekshop.ru',
             'address': 'В пределах центра'},
        ]

        context = {
            'page_title': 'контакты',
            'locations': locations,
        }
        return render(request, 'mainapp/contact.html', context)
