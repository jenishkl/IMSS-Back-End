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
from newapp.view_s.locationview import LocationView
from newapp.view_s.myCategoryView import MyCategoryView,createMyCategory
from newapp.view_s.mainCategoryView import getCategory
from newapp.view_s.shopViews import edit_shop,get_shops
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('product', views.ProductView, 'product')
# router.register("maincategory", views.MainCategoryView, "maincategory")
router.register("shopregister", views.ShopRegisterView, "shopregister")
router.register("products", views.ProductsView, "products")
router.register("location", LocationView, "location")
router.register("mycategory", MyCategoryView, "mycategory")
# router.register('getshops', views.get_shops, basename='getshops')
# router.register('images', views.ImageView, 'images')
# router.register('privatecategory', views.PrivateCategoryView, 'privatecategory')
categoryCreate = views.MainCategoryView.as_view({"post": "create"})
categoryList = views.MainCategoryView.as_view({"get": "list"})
# user_list = views.ProductView.as_view({'get': 'list'})
# user_detail = views.ProductView.as_view({'get': 'retrieve'})
# post_detail = views.ProductView.as_view({'post': 'create'})
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path(
        "getshops/",
        get_shops,
    ),
    path("get_main_category/", getCategory),
    path("edit_shop/", edit_shop),
    path("create_my_category/", createMyCategory),
    # path('api-auth/', include('rest_framework.urls'))
    # path('product/',views.ProductView.as_view() )
]
# urlpatterns=router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
