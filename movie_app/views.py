from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director,Movie,Review
from movie_app.serializers import DirectorSerializer,MovieSerializer,ReviewSerializer
from rest_framework import status

@api_view(http_method_names=['GET','POST'])
def directors_list_create_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data =  DirectorSerializer(instance = directors, many = True).data
        return Response(data = {'list' : data})
    elif request.method == 'POST':
        name = request.data.get('name')
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
        director.name = request.data.get("name")
        director.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET','POST'])
def movie_list_create_api_view(request):
    if request.method == 'GET':
        movie = Movie.objects.all()
        data = MovieSerializer(instance = movie, many = True).data
        return Response(data = {'list' : data})
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        durations = request.data.get('durations')
        director_id = request.data.get('director_id')
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
        movie.title = request.data.get("title")
        movie.description = request.data.get("description")
        movie.durations = request.data.get("durations")
        movie.director_id = request.data.get("director_id")
        movie.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET','POST'])
def review_list_api_create_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(instance = reviews, many = True).data
        return Response(data = {'list' : data})
    elif request.method == 'POST':
        text = request.data.get('text')
        movie_id = request.data.get('movie_id')
        stars = request.data.get('stars')
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
        review.text = request.data.get("text")
        review.movie_id = request.data.get("movie_id")
        review.stars = request.data.get("stars")
        review.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET'])
def movie_list_review_api_view(request):
    movie = Movie.objects.all()
    data = MovieSerializer(instance = movie, many = True).data
    return Response({'movies': data})



