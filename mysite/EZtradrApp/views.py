from django.shortcuts import render, render_to_response, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Watch, Asset, WatchAsset
from .serializers import UserSerializer, WatchSerializer, AssetSerializer, WatchAssetSerializer

from pandas_datareader import data, wb
import pandas_datareader as web

import pandas_datareader.data as web
import datetime

class UserAPI(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        users = User.objects.delete(pk)
        return Response(users, status=status.HTTP_200_OK)


class WatchAPI(APIView):
    def get(self, request):
        watch = Watch.objects.all()
        serializer = WatchSerializer(watch, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = WatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    def delete(self, request, pk, format=None):
        watch = Watch.objects.delete(pk)
        watch.delete()
        return Response(watch, status=status.HTTP_200_OK)


class AssetAPI(APIView):
    def get(self, request):
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        assets = Asset.objects.delete(pk)
        return Response(assets, status=status.HTTP_200_OK)


class WatchAssetAPI(APIView):
    def get(self, request):
        assets = WatchAsset.objects.all()
        serializer = WatchAssetSerializer(assets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchAssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        assets = WatchAsset.objects.delete(pk)
        return Response(assets, status=status.HTTP_200_OK)

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
'''


# Create your views here.
def index (request):
    return render_to_response('index.html')
