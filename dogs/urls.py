from django.urls import path
from rest_framework import routers

from dogs.views.dog import *
from dogs.views.breed import *

from dogs.apps import DogsConfig

app_name = DogsConfig.name

urlpatterns = [
    path('', DogListView.as_view()),
    path('<int:pk>/', DogDetailView.as_view()),
    path('create/', DogCreateView.as_view()),
    path('<int:pk>/update/', DogUpdateView.as_view()),
    path('<int:pk>/delete/', DogDeleteView.as_view()),
]

router = routers.SimpleRouter()
router.register('breed', BreedViewSet)

urlpatterns += router.urls
