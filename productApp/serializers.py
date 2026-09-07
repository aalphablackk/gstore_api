from rest_framework import serializers

from accounts.models import CustomUser
from .models import Category, Brand, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        # fields = "__all__" 
        fields = ["id" ,"name"]



class BrandSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # rep['category']= CategorySerializer(instance.category).data
        rep['category']= instance.category.name
       
        return rep

    class Meta:
        model = Brand
        fields = ["id" ,"name"]
        # fields = "__all__" 
        # fields = ["category" ,"name"]


class ProductSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['brand']= BrandSerializer(instance.brand).data
        # rep['brand']= instance.brand.name
        rep['brand']= {
            'id' : instance.brand.id,
            'name' : instance.brand.name,
            'category_name': instance.brand.category.name
        }
        image = None
        if rep['image'] : 
            image = rep['image']
        elif rep['image_link']:
            image = rep['image_link']

        rep.pop('image')
        rep.pop('image_link')

        rep['image'] = image

        return rep

    def validate(self, attrs):
        if attrs.get('image') and attrs.get('image_link'):
            raise serializers.ValidationError("You can either use image link or upload image")
        return super().validate(attrs)

    class Meta:
        model = Product
        fields = "__all__" 
        read_only_fields = ['created_at', 'updated_at']
        # fields = ["category" ,"name"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name','phone_number', 'is_verified', 'created_at', 'updated_at']
        read_only_fields = ['id', 'email','is_active','is_verified', 'created_at', 'updated_at']

