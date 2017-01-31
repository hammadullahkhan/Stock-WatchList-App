from django.shortcuts import render, render_to_response, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Stock, Watch
from .serializers import StockSerializer, WatchSerializer

from pandas_datareader import data, wb
import pandas_datareader as web

import pandas_datareader.data as web
import datetime

class StockAPI(APIView):
    def get(self, request):
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    '''
    def delete(self, request):
        stocks = Stock.objects.all().delete()
        return Response(stocks, status=status.HTTP_200_OK)
    '''

class WatchAPI(APIView):
    def get(self, request):
        watch = Watch.objects.all()
        serializer = WatchSerializer(watch, many=True)
        return Response(serializer.data)

    def post(self, request):
        print ('watch adding now')
        serializer = WatchSerializer(data=request.data)
        print (serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    '''
    def delete(self, request, pk, format=None):
        watch = Watch.get_object(pk)
        watch.delete()
        return Response(watch, status=status.HTTP_200_OK)
    '''



class PandasAPI(APIView):

    def get(self, request):

        stocksData = {}
        stockslist = []
        start = datetime.datetime(2017, 1, 27)
        end = datetime.datetime(2017, 12, 31)

        watchList = Watch.objects.all()
        for watch in watchList:
            stockslist.append(str(watch))


        for ticker in stockslist:
            stocksData[ticker] = web.DataReader(ticker, "yahoo", start, end)
            curTicker = stocksData[ticker]
            loopLenX = len( curTicker["Open"] )

            for x in range(loopLenX):

                date = str(curTicker.index[x])[0:10]

                data_open, data_high, data_low, data_close, data_volume, data_adjClose = str(curTicker["Open"][x]), str(curTicker["High"][x]), str(curTicker["Low"][x]), str(curTicker["Close"][x]), str(curTicker["Volume"][x]), str(curTicker["Adj Close"][x])
                data = {'ticker': ticker, 'date': date, 'open': data_open, 'close': data_close, 'volume': data_volume, 'high': data_high, 'low': data_low, 'adjClose': data_adjClose}

                serializer = StockSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()


        return Response(stocksData)



# Create your views here.
def index (request):
    return render_to_response('index.html')
