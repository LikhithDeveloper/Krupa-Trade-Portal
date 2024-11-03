"""
URL configuration for krupatrade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from krupa.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register_view,name='register_view'),
    path('orderdetails/<int:id>/',order_details_view,name='order_details_view'),
    path('orders/<int:id>/',order_view,name='order_view'),
    path('',products_view,name="products_view"),
    path('login/',login_view,name='login_view'),
    path('request/<int:id>/',request_view,name="request_view"),
    path('support/<int:id>/',support_ticket_view_1,name="support_ticket_view_1"),
    path('support_create/<int:id>/',support_ticket_view_2,name="support_ticket_view_2"),
    path('accounts/<int:id>/',account_view,name='accounts'),
    path('invoice/<int:id>/',invoice_view,name="invoice_view"),
    path('dashboard/',dashboard_view,name="dashboard_view"),
    path('trackhome/',TrackHome,name="TrackHome"),
    path('trackorder/',TrackOrder,name="TrackOrder"),

    path('',include('admin_panel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
