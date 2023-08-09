from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.relations import SlugRelatedField

from dogs.models import Breed, Dog


class DogListSerializer(serializers.ModelSerializer):
    breed = SlugRelatedField(slug_field="name", queryset=Breed.objects.all())

    class Meta:
        model = Dog
        fields = ("name", "breed",)


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = "__all__"


class BreedListSerializer(serializers.ModelSerializer):
    dog_count = IntegerField()  # 2) для метода без дополнительного обращения к БД
    class Meta:
        model = Breed
        fields = ("name", "dog_count")


class BreedDetailSerializer(serializers.ModelSerializer):
    dog_this_breed = SerializerMethodField()

    def get_dog_this_breed(self, breed):
        # return [dog.name for dog in Dog.objects.filter(breed=breed)]  # выдает список имен собак заданной породы
        return DogListSerializer(Dog.objects.filter(breed=breed), many=True).data

    class Meta:
        model = Breed
        fields = "__all__"
