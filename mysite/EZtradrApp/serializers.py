from rest_framework import serializers
from .models import User, Watch, Asset, WatchAsset


class UserSerializer(serializers.ModelSerializer):

    userId = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = '__all__'


class WatchSerializer(serializers.ModelSerializer):

    watchId = serializers.ReadOnlyField()
    class Meta:
        model = Watch
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):

    assetId = serializers.ReadOnlyField()
    class Meta:
        model = Asset
        fields = '__all__'


class WatchAssetSerializer(serializers.ModelSerializer):

    watchAssetId = serializers.ReadOnlyField()
    class Meta:
        model = WatchAsset
        fields = '__all__'
