from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:product_slug>/',views.CategoryView.as_view(), name='category_view'),
    path('prduct_type/',views.ProductListByTypeView.as_view(), name='product_type'),
]