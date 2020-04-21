from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from carts.models import Cart
from .models import Product
# Create your views here.


class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context["title"] = "Product List"
        # print(context)
        return context
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)


class ProductFeaturedListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductFeaturedDetailView(DetailView):
    # queryset = Product.objects.all()
    template_name = "products/featured-detail.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductDetailView(DetailView):
    # queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)

        # print(context)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get("pk")

        prod_object = Product.objects.get_by_id(pk)

        if prod_object is None:
            raise Http404("Product does not exist")
        self.extra_context["title"] = prod_object.title
        return prod_object


class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, **kwargs):
        context = context = super(ProductDetailSlugView, self).get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context


    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")

        # prod_object = get_object_or_404(Product, slug=slug)
        try:
            prod_object = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Not Found")
        except Product.MultipleObjectsReturned:
            queryset = Product.objects.filter(slug=slug)
            prod_object = queryset.first
        except:
            raise Http404("Something went wrong.")

        if prod_object is None:
            raise Http404("Product does not exist")

        self.extra_context = {"title" : prod_object.title}
        return prod_object


def product_detail_view(request, pk):
    # prod_object = Product.objects.get(pk=pk)  # primary key == id usually
    # prod_object = get_object_or_404(Product, pk=pk)
    # try:
    #     prod_object = Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     print(f"No product with id {pk}")
    #     raise Http404("Product does not exist")
    # except:
    #     print("something weird happened")
    prod_object = Product.objects.get_by_id(pk)

    # qs = Product.objects.filter(pk=pk)
    if prod_object is None:
        raise Http404("Product does not exist")
    context = {
        'object': prod_object
    }
    return render(request, "products/detail.html", context)

