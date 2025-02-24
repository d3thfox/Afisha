from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director,Movie,Review
from movie_app.serializers import DirectorSerializer,MovieSerializer,ReviewSerializer,MovieValidSerializer,DirectorValidSerializer
from movie_app.serializers import ReviewValidSerializer
from rest_framework import status
from django.db.models import Avg  
from django.db.models import Count
from django.db import transaction 
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

class DirectosListApiView(ListCreateAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = DirectorValidSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        name = serializer.validated_data.get('name')

        with transaction.atomic():
            director = Director.objects.create(name=name)
            director.save()
            return Response(data ={'director_id' : director.id }, status = status.HTTP_201_CREATED)

    
    


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorValidSerializer
    queryset = Director.objects.all()
    lookup_field = 'id'

class MovieViewAPIView(ListCreateAPIView):
    serializer_class = MovieValidSerializer
    queryset = Movie.objects.select_related("director").prefetch_related("reviews").annotate(avg_rating = Avg('reviews__stars')).all()
    def create(self, request, *args, **kwargs):
        serializer = MovieValidSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(status = status.HTTP_400_BAD_REQUEST, data = serializer.errors)
        
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        durations = serializer.validated_data.get('durations')
        director_id = serializer.validated_data.get('director_id')
       
        with transaction.atomic():
            movie = Movie.objects.create(title=title, description=description, durations=durations, director_id=director_id)
            movie.save()
            return Response(data = {'movie_id' : movie.id}, status = status.HTTP_201_CREATED)
       
       



class MovieDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieValidSerializer
    queryset = Movie.objects.select_related("director").prefetch_related("reviews").annotate(avg_rating = Avg('reviews__stars')).all()
    lookup_field = 'id'

class ReviewListReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewValidSerializer
    queryset = Review.objects.select_related('movie')


    
    def create(self, request, *args, **kwargs):
        serializer = ReviewValidSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(status = status.HTTP_400_BAD_REQUEST,data = serializer.errors )
        text = serializer.validated_data.get('text')
        movie_id = serializer.validated_data.get('movie_id')
        stars = serializer.validated_data.get('stars')
        
        with transaction.atomic():
            review = Review.objects.create(text=text, movie_id=movie_id, stars=stars)
            review.save()
            return Response(data = {'review_id' : review.id}, status = status.HTTP_201_CREATED)
        

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewValidSerializer
    queryset = Review.objects.select_related('movie')
    lookup_field = 'id'


class MovieListReviewsApiView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Movie.objects.select_related("director").prefetch_related("reviews").annotate(avg_rating = Avg('reviews__stars'))

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(status = status.HTTP_400_BAD_REQUEST, data = serializer.errors)
        
        movie_id = serializer.validated_data.get('movie_id')
       
        with transaction.atomic():
            review = Review.objects.create(movie_id=movie_id, **serializer.validated_data)
            review.save()
            return Response(data = {'review_id' : review.id}, status = status.HTTP_201_CREATED)


    # for query in connection.queries:
    #     print(query["sql"]) проверка на дубликаты в БД :3




