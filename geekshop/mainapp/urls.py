from django.urls import path, re_path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.Index.as_view(), name='index'),
    path('new/', mainapp.Index.as_view(), name='index_new'),
    path('products/', mainapp.Products.as_view(), name='products'),
    path('contact/', mainapp.Contact.as_view(), name='contact'),
    path('category/<int:pk>/', mainapp.Category.as_view(), name='category'),
    path('product/<int:pk>/', mainapp.ProductPage.as_view(), name='product_page'),
    path('product/<int:pk>/price/', mainapp.get_product_price),
]
