from django.utils import timezone
from django.shortcuts import render,redirect
from food_items.models import MenuItem,Order,OrderItem


def menupage(request):
    menudetails=MenuItem.objects.all()

    return render(request,'menu.html',{'menudetails':menudetails})


def cart(request):
    session_cart=request.session.get('cart',{})
    cart_items=[]
    total_price=0
 
   

    for item_id,quantity in session_cart.items():
        try:
            item=MenuItem.objects.get(id=item_id)
            item.quantity=quantity
            item.total=item.price*quantity
            cart_items.append(item)
            total_price+=item.total
        except MenuItem.DoesNotExist:
            continue

    return render (request,'cart.html',{'cart_items':cart_items,'total_price':total_price})

def add_to_cart(request,item_id):
    print("Add to Cart called for ID:", item_id)

    if request.method=="POST":
        quantity=int(request.POST.get('quantity',1))
        print("Quantity received:", quantity)
        cart=request.session.get('cart',{})
        print("Old cart:", cart)   
        if str(item_id) in cart:
            cart[str(item_id)] += quantity
        else:
            cart[str(item_id)] = quantity

        request.session['cart'] = cart 
        print("Updated cart:", cart)  

        return redirect('cart')
    else:
        return redirect('menupage')
    

def update_cart(request, item_id):
    if request.method == "POST":
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if str(item_id) in cart:
            if action == "increase":
                cart[str(item_id)] += 1
            elif action == "decrease":
                if cart[str(item_id)] > 1:
                    cart[str(item_id)] -= 1
                else:
                    del cart[str(item_id)]

        request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, item_id):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        if str(item_id) in cart:
            del cart[str(item_id)]
            request.session['cart'] = cart
    return redirect('cart')



def checkout(request):
    total_price=0
    cart_items=[]
    session_cart = request.session.get('cart', {})

    if not session_cart:
        return redirect('cart')  # agar cart khali hai toh redirect
    
  
    for item_id, quantity in session_cart.items():
        try:
            item=MenuItem.objects.get(id=item_id)
            item.quantity=quantity
            item.total=item.price*quantity
            cart_items.append(item)
            total_price+=item.total
        except MenuItem.DoesNotExist:
            continue


    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Order create karo
        order = Order.objects.create(
            customer_name=name,
            phone=phone,
            address=address,
            order_date=timezone.now()
        )

        for item in cart_items:
            order_item = OrderItem.objects.create(
                menu_item=item,
                quantity=item.quantity
            )
            order.items.add(order_item)

        # Cart clear karo
        request.session['cart'] = {}

        return render(request, 'order_success.html', {'order': order})

    return render(request, 'order_summary.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })



