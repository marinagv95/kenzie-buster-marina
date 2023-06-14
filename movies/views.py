from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from movies.models import Movie
from movies.serializer import MovieSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsAdminOrReadOnly



class MovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get_movie(self, movie_id):
        return get_object_or_404(Movie, id=movie_id)

    def get(self, request, movie_id):
        movie = self.get_movie(movie_id)
        return Response(MovieSerializer(movie).data)

    def delete(self, request, movie_id):
        movie = self.get_movie(movie_id)
        
        if not IsAdminOrReadOnly().has_object_permission(request, self, movie):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
