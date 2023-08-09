from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.relations import SlugRelatedField
from dogs.serializers.breed import BreedDetailSerializer

from dogs.models import Dog, Breed


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = "__all__"


class DogDetailSerializer(serializers.ModelSerializer):
    breed = BreedDetailSerializer()
    dog_with_same_breed = SerializerMethodField()  # 1) данный метод делает еще 1 запрос в БД (что замедляет работу)

    def get_dog_with_same_breed(self, dog):
        return Dog.objects.filter(breed=dog.breed).count()

    class Meta:
        model = Dog
        fields = ("name", "breed", "dog_with_same_breed")
