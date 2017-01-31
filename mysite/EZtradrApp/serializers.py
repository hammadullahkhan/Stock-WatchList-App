from rest_framework import serializers
from .models import Stock, Watch

class StockSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    class Meta:
        model = Stock
        fields = ('id', 'ticker', 'volume', 'open', 'close', 'high', 'low', 'adjClose', 'date')
        #fields = '__all__'

class WatchSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    class Meta:
        model = Watch
        fields = ('id', 'ticker',)
        #fields = '__all__'
