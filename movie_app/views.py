from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director,Movie,Review
from movie_app.serializers import DirectorSerializer,MovieSerializer,ReviewSerializer,MovieValidSerializer,DirectorValidSerializer
from movie_app.serializers import ReviewValidSerializer
from rest_framework import status
from django.db.models import Avg  
from django.db.models import Count

@api_view(http_method_names=['GET','POST'])
def directors_list_create_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.annotate(movies_count=Count("movies")).all()
        data =  DirectorSerializer(instance = directors, many = True).data
        return Response(data = {'list' : data})
    elif request.method == 'POST':
        serializer = DirectorValidSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        name = serializer.validated_data.get('name')
        director = Director.objects.create(name = name)
        return Response(data = {'director_id' : director.id})


@api_view(http_method_names=['GET','PUT','DELETE']) 
def directors_detail_update_api_view(request, id):
    try:
        director = Director.objects.get(id = id)
    except Director.DoesNotExist:
        return Response(data = {'erros' : 'director not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(instance = director, many = False).data
        return Response(data = data)
    elif request.method == 'PUT':
        serializer = DirectorValidSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        director.name = serializer.validated_data.get("name")
        director.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET','POST'])
def movie_list_create_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.select_related("director").prefetch_related("reviews").annotate(avg_rating = Avg('reviews__stars')).all()
        data = MovieSerializer(instance = movies, many = True).data
        return Response(data = {'list' : data})
    elif request.method == 'POST':
        serializer = MovieValidSerializer(data = request.data)
        if not serializer.is_valid():
                    return Response(status = status.HTTP_400_BAD_REQUEST,data = serializer.errors )
        
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        durations = serializer.validated_data.get('durations')
        director_id = serializer.validated_data.get('director_id')
        movie = Movie.objects.create(title=title, description=description,durations=durations, director_id=director_id)
        return Response(data = {'movie_id' : movie.id}, status = status.HTTP_201_CREATED)

@api_view(http_method_names=['GET','PUT','DELETE'])
def movie_detail_update_api_view(request, id):
    try:
        movie = Movie.objects.get(id = id)
    except Movie.DoesNotExist:
        return Response(data = {'erros' : 'Movie not found'},
                        status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = MovieSerializer(instance = movie, many = False).data
        return Response(data = data)
    
    elif request.method == 'PUT':
        serializer = MovieValidSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(status = status.HTTP_400_BAD_REQUEST,data = serializer.errors )
        movie.title = serializer.validated_data.get("title")
        movie.description = serializer.validated_data.get("description")
        movie.durations = serializer.validated_data.get("durations")
        movie.director_id = serializer.validated_data.get("director_id")
        movie.save()
        return Response(status=status.HTTP_201_CREATED)
    
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET','POST'])
def review_list_api_create_view(request):
    if request.method == 'GET':
        reviews = Review.objects.select_related('movie')
        data = ReviewSerializer(instance = reviews, many = True).data
        return Response(data = {'list' : data})
    elif request.method == 'POST':
        serializer = ReviewValidSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(status = status.HTTP_400_BAD_REQUEST,data = serializer.errors )
        text = serializer.validated_data.get('text')
        movie_id = serializer.validated_data.get('movie_id')
        stars = serializer.validated_data.get('stars')
        review = Review.objects.create(text=text, movie_id=movie_id, stars=stars)
        return Response(data = {'review_id' : review.id}, status = status.HTTP_201_CREATED)
    
@api_view(http_method_names=['GET','PUT','DELETE'])
def review_detail_update_api_view(request, id):
    try:
        review = Review.objects.get(id = id)
    except Review.DoesNotExist:
        return Response(data = {'erros' : 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(instance = review, many = False).data
        return Response(data = data)
    elif request.method == 'PUT':
        serializer = ReviewValidSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(status = status.HTTP_400_BAD_REQUEST,data = serializer.errors )
        review.text = serializer.validated_data.get("text")
        review.movie_id = serializer.validated_data.get("movie_id")
        review.stars = serializer.validated_data.get("stars")
        review.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET'])
def movie_list_review_api_view(request):
    movies = Movie.objects.select_related("director").prefetch_related("reviews").annotate(avg_rating = Avg('reviews__stars'))
    data = MovieSerializer(movies, many = True).data

    # for query in connection.queries:
    #     print(query["sql"]) проверка на дубликаты в БД :3

    return Response({'movies': data})



