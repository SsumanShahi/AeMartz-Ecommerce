from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from math import ceil
import json
# import the logging library
import logging

# Create your views here.
def show_products(request):
    # products=Product.objects.all()
    # print(products)
    # n =len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    allprods=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        products=Product.objects.filter(category=cat)
        n =len(products)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allprods.append([products,range(1,nSlides),nSlides])

    # context={
    #     'no_of_slides':nSlides,
    #     'range':range(1,nSlides),
    #     'products':products
    # }
    # allprods=[[products,range(1,nSlides),nSlides],[products,range(1,nSlides),nSlides]]
    context={'allprods': allprods}
    return render(request,'ecommerce/index.html',context)

def searchMatch(query,item):
    # return ture only if query matches the item
    if query in item.product_desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
def Search(request):
    query=request.GET.get('search')
    allprods=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        productstemp=Product.objects.filter(category=cat)
        products= [item for item in productstemp if searchMatch(query,item)]
        n =len(products)
        nSlides = n//4 + ceil((n/4)-(n//4))
        if len(products)!=0:
            allprods.append([products,range(1,nSlides),nSlides])
    context={'allprods': allprods,"msg":""}
    if len(allprods)==0 or len(query)<4:
        context ={"msg":"Please make sure to enter relevant search query"}
    return render(request,'ecommerce/search.html',context)

def AboutUs(request):
    return render(request,"ecommerce/aboutus.html")
 
def ContactUs(request):
    thank=False
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        print(name,email,phone,desc)
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank=True
    return render(request,"ecommerce/contact.html", {'thank':thank})

def TrackingStatus(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates, "itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"no item}')
        except Exception as e:
            return HttpResponse('{"status":"error}')

    return render(request,"ecommerce/tracker.html")



def Productview(request, myid):
    # fetch the product using the id
    product=Product.objects.filter(id=myid)
    

    return render(request,"ecommerce/prodView.html",
                  {
                      'product':product[0]
                  })

def Checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'ecommerce/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user 
    return render(request,"ecommerce/checkout.html")