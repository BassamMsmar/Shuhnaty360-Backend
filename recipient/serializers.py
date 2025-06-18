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

class RecipientOptionSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.IntegerField(source='id')

    class Meta:
        model = Recipient
        fields = ['value', 'label']

    def get_label(self, obj):
        return obj.name