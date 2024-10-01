from rest_framework import serializers
from .models import Products, Orders, SupportTicket, Subcategory

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.category_name')
    subcategory_name = serializers.ReadOnlyField(source='subcategory.sub_name')

    class Meta:
        model = Products
        fields = ['id', 'product_image', 'product_name', 'category_name', 'subcategory_name', 'descripton']

class SubcategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source = 'category.category_name')

    class Meta:
        model = Subcategory
        fields = ['category','sub_name','sub_image']

class OrdersSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source = 'name.product_name')

    class Meta:
        model = Orders
        fields = ['profile','order_id','product_name','date','total']

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['order_id', 'profile', 'department', 'subject', 'message', 'additional_email', 'answered', 'created_at']

