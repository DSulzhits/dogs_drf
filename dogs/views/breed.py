from rest_framework.viewsets import ModelViewSet
from django.db.models import Count

from dogs.models import Breed
from dogs.serializers.breed import BreedDetailSerializer, BreedListSerializer, BreedSerializer


class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all()  # 1) для метода dog_with_same_breed с обращением к БД
    default_serializer = BreedSerializer
    serializers = {
        "list": BreedListSerializer,
        "retrieve": BreedDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        """Переопределение queryset 2) для метода без дополнительного обращения к БД
        "dogs" т.к. в моделях прописано related_name="dogs"""
        # self.queryset = Breed.objects.annotate(dog_count=Count("dogs"))  # 1-й способ
        self.queryset = self.queryset.annotate(dog_count=Count("dogs"))  # 2-й способ переписывается queryset строка 9
        return super().list(request, *args, **kwargs)
