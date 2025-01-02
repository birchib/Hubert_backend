from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

from .mongo_models import Person

class PersonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    age = serializers.IntegerField()

    def create(self, validated_data):
        return Person(**validated_data).save()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance