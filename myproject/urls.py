"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import path, include
from newapp import views
from newapp.view_s.locationview import LocationView, filterLocation
from newapp.view_s.checkoutViews import KartView, OrderView
from newapp.view_s.myCategoryView import MyCategoryView, createMyCategory, getMyCatgory
from newapp.view_s.productView import (
    ProductsView,
    ProductImageView,
    createProducts,
    getProducts,
    addProductImage,
)
from newapp.view_s.mainCategoryView import getCategory, filterMainCategory
from newapp.view_s.shopViews import edit_shop, get_shops
from newapp.view_s.checkoutViews import getCheckOut
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from newapp.serializer import MyTokenObtainPairSerializer

router = routers.DefaultRouter()
# router.register('product', views.ProductView, 'product')
router.register("maincategory", views.MainCategoryView, "maincategory")
router.register("shopregister", views.ShopRegisterView, "shopregister")
router.register("products", ProductsView, "products")
router.register("location", LocationView, "location")
router.register("mycategory", MyCategoryView, "mycategory")
router.register("pimage", ProductImageView, "pimage")
router.register("kart", KartView, "kart")
router.register("order", OrderView, "order")
# router.register('getshops', views.get_shops, basename='getshops')
# router.register('images', views.ImageView, 'images')
# router.register('privatecategory', views.PrivateCategoryView, 'privatecategory')
categoryCreate = views.MainCategoryView.as_view({"post": "create"})
categoryList = views.MainCategoryView.as_view({"get": "list"})
# user_list = views.ProductView.as_view({'get': 'list'})
# user_detail = views.ProductView.as_view({'get': 'retrieve'})
# post_detail = views.ProductView.as_view({'post': 'create'})
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import authentication, permissions

# class CustomTokenObtainPairView(TokenObtainPairView):
#     # Replace the serializer with your custom
#     serializer_class = MyTokenObtainPairSerializer
urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # MY CATEGORY
    path("get_main_category/", getCategory),
    path("filter-main-category/<str:pk>/", filterMainCategory),
    # LOCATION
    path("filter-/<str:pk>/", filterLocation),
    #
    path("login/", views.custom_login, name="login"),
    path("admin/", admin.site.urls),
    path(
        "",
        include(router.urls),
    ),
    # path("superadmin",include()),
    path(
        "getshops/",
        get_shops,
    ),
    path("edit_shop/", edit_shop),
    path("create_my_category/", createMyCategory),
    path("get_my_category/", getMyCatgory),
    path("product/", createProducts),
    path("get_products/", getProducts),
    path("add_product_image/", addProductImage),
    path("check_out/", getCheckOut),
    # path('api-auth/', include('rest_framework.urls'))
    # path('product/',views.ProductView.as_view() )
]
# urlpatterns=router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
