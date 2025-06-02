from rest_framework import serializers
from .models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

    def validate(self, attrs):
        if attrs['ar_city'] in [city.ar_city for city in City.objects.all()] and attrs['en_city'].lower() in [city.en_city.lower() for city in City.objects.all()]:
            raise serializers.ValidationError(
                "City with this name already exists.")
        return attrs
