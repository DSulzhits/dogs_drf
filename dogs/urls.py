from django.urls import path
from rest_framework import routers

from dogs.views.dog import *
from dogs.views.breed import *

from dogs.apps import DogsConfig

app_name = DogsConfig.name

urlpatterns = [
    # Dog
    path('', DogListView.as_view(), name='dog_list'),
    path('<int:pk>/', DogDetailView.as_view(), name='dog_detail'),
    path('create/', DogCreateView.as_view(), name='dog_create'),
    path('<int:pk>/update/', DogUpdateView.as_view(), name='dog_update'),
    path('<int:pk>/delete/', DogDeleteView.as_view(), name='dog_delete'),
    path('set_like/', SetLikeToDog.as_view(), name='dog_like')
]

router = routers.SimpleRouter()
router.register('breed', BreedViewSet)

urlpatterns += router.urls
