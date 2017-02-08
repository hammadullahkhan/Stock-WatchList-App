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


"""
User classes: List, Detail
    - List Methods: GET, POST
    - Detail Methods: GET, DELETE

    GET Example:
        http://localhost:8000/user/
        http://localhost:8000/user/16
        Response:
            {"userId":2,"name":"ibad khan","email":"ibad.khan@msn.com"}
    
    POST Example:
        Request body - key/value pair:            
            name:ibad khan
            email:ibad.khan@msn.com
        Response:
            {"userId":3,"name":"ibad khan","email":"ibad.khan@msn.com"}
"""
class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            users = User.objects.get(pk=pk)
            serializer = UserSerializer(users)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            data = {"description": "Object Not Found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):    
        try:
            user = get_object_or_404(User, pk=pk)
            user.delete()        
            data = {"deletedId": pk, "description": str(user)}
            return Response(data, status=status.HTTP_202_ACCEPTED)            
        except:
            data = {"description": "Object Not Found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


"""
Watch classes: List, Detail
    - List Methods: GET, POST
    - Detail Methods: GET, DELETE

    GET Example:
        http://localhost:8000/watch/
        http://localhost:8000/watch/16
        Response:
            {"watchId":17,"watchName":"forex","userId":1}
    
    POST Example:
        Request body - key/value pair:            
            userId:5
            watchName:forex
        Response:
            {"watchId":19,"watchName":"forex","userId":1}
"""
class WatchList(APIView):
    def get(self, request, format=None):        
        watch = Watch.objects.all()
        serializer = WatchSerializer(watch, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class WatchDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            watch = Watch.objects.get(pk=pk)
            serializer = WatchSerializer(watch)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            data = {"description": "Object Not Found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):                
        try:
            watchassets = WatchAsset.objects.all().filter(watchId=pk)
            wASerializer = WatchAssetSerializer(watchassets, many=True)                
            for wAsset in wASerializer.data:
                #print (wAsset)
                asset = get_object_or_404(Asset, assetId=wAsset['assetId'])
                asset.delete()

            watch = get_object_or_404(Watch, pk=pk)
            watch.delete()        
            data = {"deletedId": pk, "description": str(watch)}
            return Response(data, status=status.HTTP_202_ACCEPTED)      
        except:
            data = {"description": "Object Not Found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)



"""
Asset classes
    - Methods: GET, POST
    - Detail Methods: GET

    GET Example:
        http://localhost:8000/asset/
        http://localhost:8000/asset/16
        Response:
            [{"watchId":16,"watchName":"commodities","assetId":36,"assetName":"ms","volume":600,"open":"4","close":"10","low":"4","high":"5","adjClose":"5","date":"2017-02-06","userId":1,"name":"hammad","email":"hammad@msn.com"}]
    
    POST Example:
        Request body - key/value pair:            
            watchId:16
            assetName:ms
            volume:600
            open:4
            close:10
            high:5
            low:4
            adjClose:5        
            date:2017-02-06
        Response:
            {"asset":{"assetId":36,"assetName":"ms","open":"4","close":"10","volume":600,"high":"5","low":"4","adjClose":"5","date":"2017-02-06"},"watchAsset":{"watchAssetId":20,"watchId":16,"assetId":36}}
"""
class AssetList(APIView):    
    def get(self, request, format=None):
        try:
            watches = Watch.objects.all()
            wSerializer = WatchSerializer(watches, many=True)
            
            data = []
            for watch in wSerializer.data:
                user = User.objects.get(userId=watch['userId'])
                userSerializer = UserSerializer(user)

                if watch['watchId'] > 0:
                    watchassets = WatchAsset.objects.all().filter(watchId=watch['watchId'])
                    wASerializer = WatchAssetSerializer(watchassets, many=True)                
                    for wAsset in wASerializer.data:
                        if wAsset['assetId'] > 0:
                            assets = Asset.objects.all().filter(assetId=wAsset['assetId'])
                            aSer = AssetSerializer(assets, many=True)                
                            for key in aSer.data:
                                item = {'watchId': watch['watchId'], 'watchName': watch['watchName'], 'assetId': wAsset['assetId'], "assetName": key['assetName'], "volume": key['volume'], "open": key['open'], "close": key['close'], "low": key['low'], "high": key['high'], "adjClose": key['adjClose'], "date": key['date'], "userId": userSerializer.data['userId'], "name": userSerializer.data['name'], "email": userSerializer.data['email']}
                                data.append(item)


            return Response(data, status=status.HTTP_200_OK)
        except(RuntimeError, TypeError, NameError):
            data = {"description": "Object Not Found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = {'assetName': request.POST.get('assetName'), 'date': request.POST.get('date'), 'open': request.POST.get('open'), 'close': request.POST.get('close'), 'volume': request.POST.get('volume'), 'high': request.POST.get('high'), 'low': request.POST.get('low'), 'adjClose': request.POST.get('adjClose')}
        assetSerializer = AssetSerializer(data=data)
        if assetSerializer.is_valid():
            assetSerializer.save()
        else:
            return Response(assetSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = {'watchId': request.POST.get('watchId'), 'assetId': assetSerializer.data['assetId']}
        watchAssetSerializer = WatchAssetSerializer(data=data)
        if watchAssetSerializer.is_valid():
            watchAssetSerializer.save()
        else:
            return Response(watchAssetSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


        if (assetSerializer and assetSerializer.data and assetSerializer.data['assetId'] > 0) and (watchAssetSerializer and watchAssetSerializer.data and watchAssetSerializer.data['watchAssetId'] > 0):
            data = {'asset': assetSerializer.data, 'watchAsset': watchAssetSerializer.data}
            return Response(data, status=status.HTTP_201_CREATED)

        data = {'asset': assetSerializer.errors, 'watchAsset': watchAssetSerializer.errors}
        
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

class AssetDetail(APIView):    
    def get(self, request, pk, format=None):
        try:
            watch = Watch.objects.get(watchId=pk)
            wSerializer = WatchSerializer(watch)
            watch = wSerializer.data
            
            data = []
            user = User.objects.get(userId=watch['userId'])
            userSerializer = UserSerializer(user)
            
            if watch['watchId'] > 0:
                watchassets = WatchAsset.objects.all().filter(watchId=watch['watchId'])
                wASerializer = WatchAssetSerializer(watchassets, many=True)                
                for wAsset in wASerializer.data:
                    if wAsset['assetId'] > 0:
                        assets = Asset.objects.all().filter(assetId=wAsset['assetId'])
                        aSer = AssetSerializer(assets, many=True)                
                        for key in aSer.data:
                            item = {'watchId': watch['watchId'], 'watchName': watch['watchName'], 'assetId': wAsset['assetId'], "assetName": key['assetName'], "volume": key['volume'], "open": key['open'], "close": key['close'], "low": key['low'], "high": key['high'], "adjClose": key['adjClose'], "date": key['date'], "userId": userSerializer.data['userId'], "name": userSerializer.data['name'], "email": userSerializer.data['email']}
                            data.append(item)

            return Response(data, status=status.HTTP_200_OK)
        except(RuntimeError, TypeError, NameError):
            data = {"description": "Object Not Found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):    
        try:            
            asset = get_object_or_404(Asset, pk=pk)
            asset.delete()        
            data = {"deletedId": pk, "description": str(asset)}
            return Response(data, status=status.HTTP_202_ACCEPTED)     
        except:
            data = {"description": "Object Not Found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
    

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
