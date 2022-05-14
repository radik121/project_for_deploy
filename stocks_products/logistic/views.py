from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', ]
    pagination_class = LimitOffsetPagination


class StockViewSet(ModelViewSet):
    serializer_class = StockSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Stock.objects.all()
        product = self.request.query_params.get('products')
        if product is not None:
            if product.isdigit():
                queryset = queryset.filter(products=product)
            else:
                queryset = queryset.filter(products__title__icontains=product) | \
                           queryset.filter(products__description__icontains=product)

        return queryset
