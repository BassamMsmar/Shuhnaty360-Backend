from rest_framework import serializers
from .models import Client, Branch

from cities.serializers import CitySerializer

class BranchSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    class Meta:
        model = Branch
        fields = '__all__'


class ClientSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ClientSerializerDetails(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)
    class Meta:
        model = Client
        fields = '__all__'

class ClientBranchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class ClientMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']
        
class ClientBranchListSerializer(serializers.ModelSerializer):
    client = ClientMiniSerializer()
    city = CitySerializer()
    class Meta:
        model = Branch
        fields = '__all__'
class ClientBranchUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = '__all__'