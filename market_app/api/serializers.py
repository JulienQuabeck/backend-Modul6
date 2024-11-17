from rest_framework import serializers
from market_app.models import Market, Seller, Product

def validate_no_X_Y(value):
    errors=[]
    if 'X' in value:
        errors.append('no X in location')
    if 'Y' in value:
        errors.append('no Y in location')
    if errors:
        raise serializers.ValidationError(errors)
    return value

class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, validators=[validate_no_X_Y])
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    def create(self, validated_data):
        return Market.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.net_worth = validated_data.get('net_worth', instance.net_worth)
        instance.save()
        return instance
    
class SellerDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    # markets = MarketSerializer(many=True, read_only=True)
    markets = serializers.StringRelatedField(many = True)

class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child = serializers.IntegerField(), write_only = True)

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in = value)
        if len(markets) != len(value):
            raise serializers.ValidationError("One or more Marketids not found!")
        return value
    
    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller = Seller.objects.create(**validated_data)
        markets = Market.objects.filter(id__in = market_ids)
        seller.markets.set(markets)
        return seller
    
class ProductsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.StringRelatedField(many = True, read_only = True)
    seller = serializers.StringRelatedField(many = True, read_only = True)

class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    seller = serializers.PrimaryKeyRelatedField(many = True, read_only = True)

    def validate_products(self, value):
        product = Product.objects.filter(id__in = value)
        if len(product) != len(value):
            raise serializers.ValidationError("One or more productids not found!")
        return value

    def create(self, validated_data):
        market_ids = validated_data.pop('market')
        seller_ids = validated_data.pop('seller')
        product = Product.objects.create(**validated_data)
        markets = Market.objects.filter(id__in = market_ids)
        seller = Seller.objects.filter(id__in = seller_ids)
        product.market.set(markets),
        product.seller.set(seller)
        return product
        
    
# {
# "name" : "Produkt1",
# "description" : "Das erste Produkt",
# "price" : "10.00",
# "market" : [1],
# "seller" : [1,2]
# }