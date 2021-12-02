from django.shortcuts import render,redirect
from django.views.generic import View
from app.models import Product,Customer,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
 def get (self,request):
    totalitem=0
    topwears=Product.objects.filter(category='TW')
    bottomwears = Product.objects.filter(category='BW')
    mobiles = Product.objects.filter(category='M')
    laptops = Product.objects.filter(category='L')
    #totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops,'totalitem':totalitem})
#def home(request):
 #return render(request, 'app/home.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        #if request.user.is_authenticated:
        totalitem = 0
        totalitem = len(Cart.objects.filter(user=request.user))
        item_already_in_cart=Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
        print(item_already_in_cart)
        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})
#def product_detail(request):
 #return render(request, 'app/productdetail.html')

@login_required()
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    #print(product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')
@login_required()
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user=request.user
        cart=Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discounted_price)
                amount=amount+tempamount
                totalamount=amount+shipping_amount
        #print(cart_product)
            return render(request, 'app/addtocart.html',{"carts":cart,'totalamount':totalamount,"amount":amount,'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html')
def plus_cart(request):
    if request.method=='GET':
        user = request.user
        prod_id=request.GET['prod_id']#getting this id by ajax.we use ajax because by it each time page will not refresh
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0
        shipping_amount = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount=amount+tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)
    # by this JsonResponse we are sending objects to myscript.js and then it can use the quantity,amount and total amount
    #for print in output page

def minus_cart(request):
    if request.method=='GET':
        user = request.user
        prod_id=request.GET['prod_id']#getting this id by ajax.we use ajax because by it each time page will not refresh
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0
        shipping_amount = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount=amount+tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)
def remove_cart(request):
    if request.method=='GET':
        user = request.user
        prod_id=request.GET['prod_id']#getting this id by ajax.we use ajax because by it each time page will not refresh
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0
        shipping_amount = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount=amount+tempamount
        data={
            'amount':amount,
            'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)
def buy_now(request):
 return render(request, 'app/buynow.html')

#def profile(request):
 #return render(request, 'app/profile.html')
@login_required()
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':"btn-primary"})
@login_required()
def orders(request):
    totalitem = 0
    totalitem = len(Cart.objects.filter(user=request.user))
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{"order_placed":op,'totalitem':totalitem})

def mobile(request,data=None):
    totalitem = 0
    totalitem = len(Cart.objects.filter(user=request.user))
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=="Sony" or data=="Huawei" or data=="Apple" or data=="Samsung":
        mobiles= Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data=='above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html',{"mobiles":mobiles,'totalitem':totalitem})

def laptop(request,data=None):
    totalitem = 0
    totalitem = len(Cart.objects.filter(user=request.user))
    if data==None:
        laptop=Product.objects.filter(category='L')
    elif data=="Lenovo" or data=="Dell" or data=="Hp" or data=="Asus":
        laptop= Product.objects.filter(category='L').filter(brand=data)
    elif data=='below':
        laptop = Product.objects.filter(category='L').filter(discounted_price__lt=25000)
    elif data=='above':
        laptop = Product.objects.filter(category='L').filter(discounted_price__gt=25000)
    return render(request, 'app/laptop.html',{"laptop":laptop,'totalitem':totalitem})

def bottomwear(request,data=None):
    totalitem = 0
    totalitem = len(Cart.objects.filter(user=request.user))
    if data==None:
        bottomwear=Product.objects.filter(category='BW')
    elif data=="Wrangler" or data=="Diesel" or data=="Pepe":
        #data == "Levi's"
        bottomwear=Product.objects.filter(category='BW').filter(brand=data)
    elif data=='below':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt=1000)
    elif data=='above':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__gt=500)
    return render(request, 'app/bottomwear.html',{"bottomwear":bottomwear,'totalitem':totalitem})
def topwear(request,data=None):
    totalitem = 0
    totalitem = len(Cart.objects.filter(user=request.user))
    if data==None:
        topwear=Product.objects.filter(category='TW')
    elif data=="Biba" or data=="Fabindia" or data=="westside":
        topwear=Product.objects.filter(category='TW').filter(brand=data)
    elif data=='below':
        topwear = Product.objects.filter(category='TW').filter(discounted_price__lt=500)
    elif data=='above':
        topwear = Product.objects.filter(category='TW').filter(discounted_price__gt=500)
    return render(request, 'app/topwear.html',{"topwear":topwear,'totalitem':totalitem})

#def login(request):
 #return render(request, 'app/login.html')here we are using the authenticationForm so no
    # need to define in view we can directly show in url.py

#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self,request):
        form =CustomerRegistrationForm
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form =CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!!Registered Successfully...')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

#def reset(request):
    #return render(request,"app/login.html")
@method_decorator(login_required,name="dispatch")
class ProfileView(View):
    def get(self,request):
        totalitem = 0
        totalitem = len(Cart.objects.filter(user=request.user))
        form=CustomerProfileForm
        return render(request,'app/profile.html',{'form':form,'active':"btn-primary",'totalitem':totalitem})

    def post(self,request):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user#for currently log inned user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulation Profile updated successfully")
        return render(request,"app/profile.html",{"form":form,'active':"btn-primary"})
@login_required()
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount = 0
    shipping_amount = 70
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount = amount + tempamount
        totalamount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,"cart_items":cart_items})
@login_required()
def payment_done(request):
    user=request.user
    custid=request.GET.get("custid")#for two different address id is different
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")