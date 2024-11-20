from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, SellerSerializer, ProductsSerializer, ProductCreateSerializer
from market_app.models import Market, Seller, Product

@api_view(['GET', 'POST'])
def markets_view(request):

    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = SellerSerializer(markets, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer= SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

@api_view(['GET', 'DELETE', 'PUT'])
def market_single_view(request, pk):

    if request.method == 'GET':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    if request.method == 'DELETE':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market)
        market.delete()
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
def sellers_view(request):
    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer= SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
@api_view(['GET', 'PUT', 'Delete'])
def sellers_single_view(request, pk):
    if request.method == 'GET':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        seller = Seller.objects.get(pk=pk)
        seller.delete()
        return Response({'message' : 'Seller deleted successfully!'}, status = 204)

        # serializer = SellerSerializer(seller)
        # seller.delete()
        # return Response(serializer.data)

@api_view(['GET', 'POST'])
def products_view(request):
    pass
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer= ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)