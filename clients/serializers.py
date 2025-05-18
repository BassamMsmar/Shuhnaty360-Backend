from rest_framework import serializers
from .models import Client, Branch



class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
class ClientSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)
    class Meta:
        model = Client
        fields = '__all__'

class ClientBranchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
class ClientBranchListSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='name', read_only=True)
    city = serializers.SlugRelatedField(slug_field='ar_city', read_only=True)
    class Meta:
        model = Branch
        fields = '__all__'