from django.contrib import admin
from django.urls import path
from admin_panel.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminproducts/',AdminProducts,name="AdminProducts"),
    path('addproducts/',AddProducts,name="AddProducts"),
    path('addsubcategories/',AddSubCategories,name="AddSubCategories"),
    path('addcategories/',AddCategories,name="AddCategories"),
    path('leadsall/',Leads1,name='Leads1'),
    path('leadsbuyer/',Leads2,name='Leads2'),
    path('leadsseller/',Leads3,name='Leads3'),
    path('customerspage/',Customers,name='Customers'),
    path('managers/',ManagersView,name="ManagersView"),
    path('addmanagers/',AddManagers,name="AddManagers"),
    path('estimates/',Estimates,name="Estimates"),
    path('estimates2/',Estimates2,name="Estimate2"),
    path('newestimates/',Newestimates,name='Newestimates'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)