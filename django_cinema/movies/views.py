from rest_framework import generics, permissions, viewsets
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

#################################3
from .models import Movie
from .serializers import *
from .service import *
# Create your views here.

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = PaginationMovies
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров или режиссеров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer


# class MovieListView(generics.ListAPIView):
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend, )
#     filterset_class = MovieFilter
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user =models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         return movies


# class MovieDetailView(generics.RetrieveAPIView):
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
    

# class ReviewCreateView(generics.CreateAPIView):
#     serializer_class = ReviewCreateSerializer


# class AddStarRatingView(generics.CreateAPIView):

#     serializer_class = CreateRatingSerializer
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))



# class ActorsListView(generics.ListAPIView):
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer

# class ActorsDetailView(generics.RetrieveAPIView):
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer