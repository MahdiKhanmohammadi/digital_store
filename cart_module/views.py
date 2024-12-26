from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from product_module.models import Product, Discount
from .models import Cart, CartItem
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.emailService import send_email

# Create your views here.


def show_cart(request: HttpRequest):
    if request.user.is_authenticated:

        user = request.user
        get_user_cart = Cart.objects.filter(user=user, state=False)

        if get_user_cart:
            get_user_cart = get_user_cart[0]
            get_user_cart.discount = None
            get_user_cart.calculating_total_price()

            items = get_user_cart.items.all()

            context = {
                'item_count': items.count,
                'items': items,
                'cart': get_user_cart
            }
            return render(request, "cart_module/cart.html", context)
        else:
            new_cart = Cart(user = user)
            new_cart.save()
            context = {
                'item_count': 0,
                'items': None,
                'cart': new_cart
            }
            return render(request, "cart_module/cart.html", context)

    else:
        return HttpResponseNotFound()


def add_product_to_cart(request: HttpRequest):

    if request.user.is_authenticated:

        pk = request.GET.get('pk')

        find_product = get_object_or_404(Product, pk=pk)

        user = request.user

        get_user_cart = Cart.objects.filter(user=user, state=False)

        if get_user_cart:
            get_user_cart = get_user_cart[0]

            item_in_cart = get_user_cart.items.filter(product=find_product)

            if item_in_cart:
                item_in_cart = item_in_cart[0]

                item_in_cart.quantity += 1

                item_in_cart.price = item_in_cart.total_price()

                item_in_cart.save()

                get_user_cart.calculating_total_price()

                result = {
                    "quantity": item_in_cart.quantity,
                    "price": item_in_cart.price,
                    "total_price": get_user_cart.total_price
                }

                return JsonResponse(result)
            else:
                CartItem.add_item_to_cart(get_user_cart, find_product)

        else:
            new_cart = Cart.objects.create(user=user)
            new_cart.save()
            CartItem.add_item_to_cart(new_cart, find_product)

        return HttpResponse("محصول با موفقیت افزوده شده.")
    else:
        return HttpResponse('404')


def remove_product_in_cart(request):
    if request.user.is_authenticated:

        pk = int(request.GET.get('pk'))

        find_product = get_object_or_404(Product, pk=pk)

        user = request.user

        get_user_cart = Cart.objects.filter(user=user, state=False)

        if get_user_cart:
            get_user_cart = get_user_cart[0]

            item_in_cart = get_user_cart.items.filter(product=find_product)
            if item_in_cart:
                item_in_cart = item_in_cart[0]
                if item_in_cart.quantity > 1:
                    item_in_cart.quantity -= 1
                    item_in_cart.price = item_in_cart.total_price()
                    item_in_cart.save()

                    get_user_cart.calculating_total_price()

                    result = {
                        "quantity": item_in_cart.quantity,
                        "price": item_in_cart.price,
                        "total_price": get_user_cart.total_price

                    }
                    return JsonResponse(result)
                elif item_in_cart.quantity == 1:
                    item_in_cart.delete()
                    get_user_cart.total_price = 0
                    get_user_cart.save()
                return HttpResponse("remove")


def complete_remove(request: HttpRequest):
    if request.user.is_authenticated:
        user = request.user

        primary_key = int(request.GET.get('pk'))

        find_product = Product.objects.filter(pk=primary_key)

        if find_product:
            find_product = find_product[0]
            get_user_cart = Cart.objects.filter(user=user, state=False)
            if get_user_cart:
                get_user_cart = get_user_cart[0]
                cart_item = get_user_cart.items.filter(
                    product=find_product)
                if cart_item:
                    cart_item[0].delete()
                    get_user_cart.calculating_total_price()

                    return HttpResponse('')
    return HttpResponseNotFound()


def discount_code(request: HttpRequest):
    if request.user.is_authenticated:
        cart_id = int(request.GET.get('pk'))
        code = request.GET.get('code')
        if code:
            get_cart = get_object_or_404(Cart, pk=cart_id)
            if get_cart.discount == None:
                check_discount = Discount.objects.filter(
                discount_code=code).exists()
                if check_discount:
                    check_discount = Discount.objects.get(
                    discount_code=code)
                    if check_discount.check_expire_discount():
                        total_price_with_discount = check_discount.get_discount_price(
                        get_cart.total_price)
                        get_cart.total_price = total_price_with_discount
                        get_cart.discount = check_discount
                        get_cart.save()
                        data = {
                        "status": 200,
                        "price": get_cart.total_price,
                        "message": "تخفیف با موفقیت اعمال شد."
                    }
                        return JsonResponse(data)
                    else:
                        data = {
                        "status": 404,
                        "message": "تاریخ اعتبار کد تخفیف گذشته است."
                    }
                        return JsonResponse(data)
                else:
                    data = {
                    "status": 404,
                    "message": "کد تخفیف وجود ندارد."
                }
                    return JsonResponse(data)
        else :
            data = {
                    "status": 404,
                    "message": "کد تخفیف وجود ندارد."
                }
            return JsonResponse(data)
    else:
        return HttpResponseNotFound()
    def change_state(request:HttpRequest):
        if request.user.is_authenticated and request.method == "POST":
            pk = request.POST.get('cart_id')
            cart = get_object_or_404(Cart,pk = pk)
            cart.state = 1 
            cart.save()
            return redirect('home')
        else:
            return HttpResponseNotFound()

@receiver(post_save,sender = Cart)
def checkout(sender,instance,**kwargs):
    if instance.state == 1:
        send_email('email/checkout.html',instance.user.email,{"tracking_code" :instance.tracking_code},"تسویه سبد خرید")
