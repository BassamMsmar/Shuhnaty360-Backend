from rest_framework import serializers
from .models import City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


    def validate(self, attrs):
        if attrs['name'].lower() in [city.name.lower() for city in City.objects.all()]:
            raise serializers.ValidationError("City with this name already exists.")
        return attrs

