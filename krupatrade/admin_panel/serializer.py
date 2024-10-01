from rest_framework import serializers
from krupa.models import Subcategory

class SubcategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source = 'category.category_name')

    class Meta:
        model = Subcategory
        fields = ['category','sub_name','sub_image']