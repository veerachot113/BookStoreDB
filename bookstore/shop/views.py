from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Product, Myrating
from django.contrib import messages
from cart.forms import CartAddProductForm
from django.db.models import Case, When

import numpy as np 
import pandas as pd

#List
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    search_term=''
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    
    if 'search' in request.GET:
        search_term = request.GET['search']
        products =  Product.objects.filter(name__icontains=search_term) 
        if products:
            messages.success(request,('You searched ') + search_term )
        else:
            messages.success(request, ('Book not found'))

    query  = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(title__icontains=query)).distinct()
        return render(request,'shop/list.html',{'products':products})

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'search_term':search_term
    }
    return render(request, 'shop/list.html', context)

#detail
def product_detail(request, id, slug):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    cart_product_form = CartAddProductForm()
    
    #rating
    if request.method == "POST":
        rate =request.POST['rating']
        ratingObject = Myrating()
        ratingObject.user = request.user
        ratingObject.product = product
        ratingObject.rating = rate
        ratingObject.save()
        messages.success(request,"Your Rating is submited ")
        return redirect('shop:product_list')

    
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }

    return render(request, 'shop/detail.html', context)
    



