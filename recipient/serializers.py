from rest_framework import serializers
from .models import Recipient

class RecipientSerializerList(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(read_only=True, slug_field='ar_city')
    class Meta:
        model = Recipient
        fields = '__all__'
class RecipientSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = '__all__'