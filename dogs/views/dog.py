from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView

from dogs.models import Dog
from dogs.serializers.breed import DogListSerializer
from dogs.serializers.dog import DogSerializer, DogDetailSerializer


class DogDetailView(RetrieveAPIView):
    queryset = Dog.objects.all()  # 1) для метода dog_with_same_breed с обращением к БД
    serializer_class = DogDetailSerializer


class DogListView(ListAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogListSerializer


class DogCreateView(CreateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class DogUpdateView(UpdateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class DogDeleteView(DestroyAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
