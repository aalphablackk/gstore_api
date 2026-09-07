from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import request, status
from rest_framework.decorators import action, api_view, permission_classes

from accounts.models import CustomUser
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework import generics, viewsets
# from rest_framework.pagination import PageNumberPagination
from .pagination import customPagination, customCursorPagination
from rest_framework.pagination import LimitOffsetPagination, CursorPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser   
from rest_framework import viewsets

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def indexView(request):
    # print(request.data)
    return Response({'message': 'Hello world'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def categoryListView(request):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many= True)
        # return Response({'data': categories}, status=status.HTTP_200_OK)
        # print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
@api_view(['GET', 'PUT', "PATCH", "DELETE"])
def categoryDetailView(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"error":"Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = CategorySerializer(data=request.data, instance=category)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = CategorySerializer(data=request.data, instance=category, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        category = Category.objects.get(id=id)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BrandView(APIView):
    # authentication_classes = [JWTAuthentication]
    # authentication_classes = []
    # get_queryset() = Brand.objects.all()
    # def get_queryset(self):
    #     return Brand.objects.all()

    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Brand.objects.all()
    


    def get(self, request, id=None):
        

        if id:
            try:
                brand = self.get_queryset().get(id=id)
                # brand = self.get_queryset()
                serializer = BrandSerializer(brand)

                return Response(serializer.data, status=status.HTTP_200_OK)
            except Brand.DoesNotExist:
                return Response({'error':'Brand Not found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            serializer = BrandSerializer(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

            

    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, id):
        try:
            brand = self.get_queryset().get(id=id)
            serializer = BrandSerializer(data=request.data, instance=brand)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Brand.DoesNotExist:
            return Response({'error':'Brand Not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request):
        try:
            brand = self.get_queryset().get(id=id)
            serializer = BrandSerializer(data=request.data, instance=brand, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Brand.DoesNotExist:
            return Response({'error':'Brand Not found'}, status=status.HTTP_404_NOT_FOUND)
                
    def delete(self, request, id):
        try:
            brand = self.get_queryset().get(id=id)
            brand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Brand.DoesNotExist:
            return Response({'error':'Brand Not found'}, status=status.HTTP_404_NOT_FOUND)
                


# GenericView

class GenericListBrandView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class GenericDetailBrandView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


# Viewsets

class BrandViewset(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'id'  #to change the pk to id



    def get_queryset(self):
        queryset = self.queryset
        query_params = self.query_params
        category_id = query_params.get("category")
        brand_name = query_params.get("brand_name")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if brand_name:
            queryset = queryset.filter(name__icontains=brand_name)
            
        return queryset

# class ProductViewset(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    # lookup_field = 'id'  #to change the pk to id
class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'  #to change the pk to id
    # pagination_class = customPagination
    # pagination_class = LimitOffsetPagination
    pagination_class = customCursorPagination


    def get_queryset(self):
        query_params = self.request.query_params
        brand_id = query_params.get('brand_id')
        if brand_id: 
            return self.queryset.filter(brand_id=brand_id)
        return self.queryset
    



# @api_view(['GET','POST'])
# def productListView(request):
#     if request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many= True)
#         return Response(serializer.data, status=status.HTTP_200_OK)



class UserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def all_users(self, request):
        users = CustomUser.objects.all()
        paginator_users = self.paginator.paginate_queryset(users, request)
        serializer = UserSerializer(users, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return self.paginator.get_paginated_response(serializer.data)
    # lookup_field = 'id'  #to change the pk to id

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def make_admin(self, request, pk=None):
        try:
            user = self.get_queryset().get(pk=pk)
            user.is_staff = True
            user.save()
            return Response({"message": "User promoted to admin successfully"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
