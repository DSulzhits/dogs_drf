from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dogs.models import Dog
from dogs.paginators import DogPaginator
from dogs.serializers.breed import DogListSerializer
from dogs.serializers.dog import DogSerializer, DogDetailSerializer
from dogs.permissions import IsDogOwner, IsModerator, IsDogPublic

from users.models import User
from dogs.tasks import send_message_about_like


class DogDetailView(RetrieveAPIView):
    queryset = Dog.objects.all()  # 1) для метода dog_with_same_breed с обращением к БД
    serializer_class = DogDetailSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsDogOwner | IsDogPublic]


class DogListView(ListAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogListSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = DogPaginator


class DogCreateView(CreateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    # permission_classes = [IsAuthenticated]


class DogUpdateView(UpdateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsDogOwner]


class DogDeleteView(DestroyAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    permission_classes = [IsAuthenticated, IsDogOwner]


class SetLikeToDog(APIView):
    def post(self, request):
        user = get_object_or_404(User, pk=request.data.get("user"))
        dog = get_object_or_404(Dog, pk=request.data.get("dog"))
        # if user in dog.likes.all():
        if dog.likes.filter(id=user.id).exists():
            return Response({"result": f"У собаки {dog} уже есть лайк от {user}"}, status=200)
        send_message_about_like.delay(user.username)
        dog.likes.add(user)
        return Response({"result": f"Лайк добавлен {dog} от {user}"}, status=200)
