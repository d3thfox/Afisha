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

     class Meta:
         model = Movie
         fields = 'id title rating reviews description durations director'.split()

     def get_rating(self, obj):
         return obj.rating
             