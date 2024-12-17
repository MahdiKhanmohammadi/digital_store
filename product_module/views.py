from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from .models import Product, Category, Comment,Blog
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound, HttpRequest, HttpResponse
from django.core.paginator import Paginator
from .forms import CommentForm
from django.contrib import messages
# Create your views here.


def product_category(request, slug):
    slug = slug

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = category.products.all()

        if products.count() < 1:
            sub = category.sub_categoires.all()
            if sub:
                for cat in sub:
                    products = products | cat.products.all()
            


        # paging
        paginator = Paginator(products, 9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            'category': category.title,
            'page_obj': page_obj
        }

        return render(request, "product_module/product_category.html", context)
    else:
        raise HttpResponseNotFound()


def articel_category(request, slug):
    slug = slug

    if slug:
        category = get_object_or_404(Category, slug=slug)
        blogs = category.blogs.all()

    # paging

        pagontaor = Paginator(blogs, 6)

        page_number = request.GET.get('page')

        page_obj = pagontaor.get_page(page_number)

        context = {
            'category': category.title,
            'page_obj': page_obj
        }
        # return HttpResponse(blogs.count())
        return render(request, "product_module/articel_category.html", context)
    else:
        raise HttpResponseNotFound()


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    category = product.categories.all()
    category = category[0]

    form = CommentForm()

    comments = product.comments.filter(visibel=True)

    similar_products = category.products.all()
    if similar_products == None:
        similar_products = category.parent.products.all()


    context = {
        'product': product,
        'category': category,
        'attributes': product.attributes.all(),
        'similar_products': similar_products,
        'comments': comments,
        'form': form,
        'user': request.user
    }

    return render(request, 'product_module/product.html', context)

def blog_detail(request,pk):
    if pk:
        get_blog = Blog.objects.filter(pk = pk)

        if get_blog:
            get_blog = get_blog[0]

            context = {
                'blog':get_blog
            }

            return render(request, 'product_module/blog.html', context)

        else:
            return HttpResponseNotFound()
    return HttpResponseNotFound()

def get_author_comment(request):
    if request.GET:
        comment_id = request.GET.get('parent_comment_id')
        try:
            comment = Comment.objects.get(pk=comment_id)
            author = comment.author.get_username()
            return HttpResponse(f"پاسخ به : {author}")
        except:
            return HttpResponse('')


def add_comment(request: HttpRequest):
    if request.POST:
        product_id = request.POST.get('product_id')
        if product_id:
            product = get_object_or_404(Product, pk=product_id)

            form = CommentForm(request.POST)
            if form.is_valid():
                comment_body = form.cleaned_data.get('comment_body')
                author = request.user
                new_comment = Comment(
                    body=comment_body, author=author, product=product)
                parent_comment_id = request.POST.get('parent_id')
                if parent_comment_id:
                    parent_comment = get_object_or_404(
                        Comment, pk=parent_comment_id)
                    new_comment.parent = parent_comment
                new_comment.save()
                messages.SUCCESS
                return redirect(reverse('product_detail', kwargs={'slug': product.slug}))
            else:
                form = CommentForm(request.POST)
                context = {'form': form}
                return render(request, 'product_module/product.html', context)
        else:
            return HttpResponseNotFound()
