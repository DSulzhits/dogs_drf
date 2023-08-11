from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from dogs.serializers.breed import BreedDetailSerializer
from dogs.validators import validator_scam_words

from dogs.models import Dog, Breed


class DogSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validator_scam_words])

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
