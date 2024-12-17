from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from product_module.models import Category, Product, Blog
from .models import Ad
from jdatetime import datetime as jdatetime
from django.db.models import Q
from django.core.paginator import Paginator


def menu_partial(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, "partial/_menu.html", context)


def home(request):

    categories = Category.objects.filter(
        parent__isnull=False).prefetch_related()

    ads = Ad.objects.filter(
        visibel=True, expire_date__gte=jdatetime.now().replace(microsecond=0)).all()

    for ad in ads:
        if ad.check_expire_date == False:
            ad.visibel = False
            ad.save()
            ads.update(ad)

    counter = 0
    ads_count = ads.count()
    for category in categories:
        if ads_count > counter:
            category.ad = ads[counter]
        else:
            break
        counter += 1

    products = Product.objects.prefetch_related().all()

    products_has_discount = products.filter(discount__isnull=False)


    for product in products_has_discount:
        product.fix_discount_state()

    most_view_product = products.order_by('-views')[:10]

    pinned_products = products.filter(pin_top=True)

    offer = products.filter(discount__isnull=False).order_by(
        '-discount__discount_percent').first()

    blogs = Blog.objects.order_by('-created_at')[:2].prefetch_related()

    context = {
        'categories': categories,
        'most_view_product': most_view_product,
        'blogs': blogs,
        'pinned_products': pinned_products,
        'offer': offer,
        'expire_date': offer.discount.discount_expire.togregorian() if offer else None
    }
    # return HttpResponse(categories)
    return render(request, 'home_module/index.html', context)


def search_product(request):
    if request.GET:
        title = request.GET.get('product_title')
        find_product = Product.objects.filter(title__icontains=title)

        # paging
        paginator = Paginator(find_product, 9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)


        context = {'products': find_product, 'page_obj': page_obj}
        return render(request, 'product_module/search_products.html', context)
