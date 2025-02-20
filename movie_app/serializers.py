from rest_framework import serializers
from movie_app.models import Director,Review,Movie

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = Director
        fields = 'id name movies_count'.split()

     
class ReviewSerializer(serializers.ModelSerializer):
     movie_name = serializers.SerializerMethodField()
     class Meta:
        model = Review
        fields = 'id text movie_name stars '.split()
    
     def get_movie_name(self, obj):
         if obj.movie:
             return obj.movie.title
         return None

     
class MovieSerializer(serializers.ModelSerializer):
     director = DirectorSerializer()
     reviews = ReviewSerializer(many=True)
     avg_rating = serializers.SerializerMethodField()  
     class Meta:
         model = Movie
         fields = 'id title avg_rating reviews description durations director'.split()
     def get_avg_rating(self, obj):
        return obj.avg_rating or 0 
        
class MovieValidSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    durations = serializers.IntegerField(min_value=1)
    director_id = serializers.IntegerField()

class DirectorValidSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class ReviewValidSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)
    movie_id = serializers.IntegerField()
    stars = serializers.IntegerField(min_value=1, max_value=5)
    