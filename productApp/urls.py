from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'brand-viewset', views.BrandViewset)
router.register(r'product-viewset', views.ProductViewset)


urlpatterns = [
    path("", views.indexView, name=""),
    path("category/", views.categoryListView, name=""),
    path("category/<int:id>/", views.categoryDetailView, name=""),
    path("brand/", views.BrandView.as_view(), name=""),
    path("brand/<int:id>/", views.BrandView.as_view(), name=""),
    path("generic-brand/", views.GenericListBrandView.as_view(), name=""),
    path("brand-detail/<int:pk>/", views.GenericDetailBrandView.as_view(), name=""),
    # path("productview/", views.productListView, name=""),
    path('', include(router.urls)),




]
