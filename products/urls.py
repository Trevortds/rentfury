from django.urls import path

from .views import (product_list_view,
                            ProductListView,
                            ProductDetailView,
                            product_detail_view,
                            ProductFeaturedDetailView,
                            ProductFeaturedListView,
                            ProductDetailSlugView)

urlpatterns = [
    path('', ProductListView.as_view(), name="list"),
    path('<slug:slug>', ProductDetailSlugView.as_view(), name="detail"),

]

# before tutorial cleanup
# urlpatterns = [
#     path('products/', ProductListView.as_view()),
#     path('featured/', ProductFeaturedListView.as_view()),
#     path('featured/<int:pk>', ProductFeaturedDetailView.as_view()),
#     path('products-fbv/', product_list_view),
#     # path('products/<int:pk>', ProductDetailView.as_view()),
#     path('products/<slug:slug>', ProductDetailSlugView.as_view()),
#     path('products-fbv/<int:pk>', product_detail_view),
#
# ]
