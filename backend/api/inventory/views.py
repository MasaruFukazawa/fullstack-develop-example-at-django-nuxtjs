# -*- coding:utf-8 -*-

from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .exception import BusinessException
from .models import Product, Purchase, Sales
from .serializers import (InventorySerializer, ProductSerializer,
                          PurchaseSerializer, SalesSerializer)


# Create your views here.
class ProductView(APIView):
    """
    商品操作に関するAPIView
    """

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound

    def get(self, request, id=None, format=None):
        """
        一覧取得用エンドポイント
        """
        if id is None:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
        else:
            product = self.get_object(id)
            serializer = ProductSerializer(product)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        登録用エンドポイント
        """
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def put(self, request, id, format=None):
        """
        更新用エンドポイント
        """
        product = self.get_object(id)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        """
        削除用エンドポイント
        """
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_200_OK)


class ProductModelViewSet(ModelViewSet):
    """
    商品操作に関するAPI(ModelViewSet)
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PurchaseView(APIView):
    """
    仕入操作関するAPI
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
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class SalesView(APIView):
    """
    売上操作関するAPI
    """

    def get(self, request, format=None):
        """
        一覧取得用エンドポイント
        """
        queryset = Sales.objects.all()
        serializer = SalesSerializer(queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        登録用エンドポイント
        """
        serializer = SalesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        purchase = Purchase.objects.filter(
            product_id=request.data["product"]
        ).aaggregate(quantity_sum=Coalesce(Sum("quantity"), 0))

        sales = Sales.objects.filter(product_id=request.data["product"]).aaggregate(
            quantity_sum=Coalesce(Sum("quantity"), 0)
        )

        if purchase["quantity_sum"] < (
            sales["quantity_sum"] + int(request.data["quantity"])
        ):
            raise BusinessException("在庫数を超過することができません")

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class InventoryView(APIView):
    """
    仕入・売上を操作するAPI
    """

    def get(self, request, id=None, format=None):
        """
        仕入・売上取得用エンドポイント
        """
        if id is None:
            return Response({}, status.HTTP_400_BAD_REQUEST)
        else:
            purchase = (
                Purchase.objects.filter(product_id=id)
                .prefetch_related("product")
                .values(
                    "id",
                    "quantity",
                    type=Value("1"),
                    date=F("purchase_date"),
                    unit=F("product__price"),
                )
            )

            sales = (
                Sales.objects.filter(product_id=id)
                .prefetch_related("product")
                .values(
                    "id",
                    "quantity",
                    type=Value("2"),
                    date=F("sales_date"),
                    unit=F("product__price"),
                )
            )

            queryset = purchase.union(sales).order_by(F("date"))
            serializer = InventorySerializer(queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
