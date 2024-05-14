# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Purchase, Sales
from .serializers import ProductSerializer, PurchaseSerializer, SalesSerializer


# Create your views here.
class ProductView(APIView):
    """
    商品操作に関するAPIView
    """

    def get(self, request, format=None):
        """
        一覧取得用エンドポイント
        """
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        登録用エンドポイント
        """
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class PurchaseView(APIView):
    """
    仕入操作関するAPI
    """

    def post(self, request, format=None):
        """
        登録用エンドポイント
        """
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class SalesView(APIView):
    """
    売上操作関するAPI
    """

    def post(self, request, format=None):
        """
        登録用エンドポイント
        """
        serializer = SalesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
