from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, Request
from rest_framework import status
from movies.models import Movie
from movies.serializer import MovieOrderSerializer, MovieSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import CustomIsAuthenticated, IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.pagination import PageNumberPagination



class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()
        pages_results = self.paginate_queryset(movies, request)
        serializer = MovieSerializer(instance=pages_results, many=True)
        return self.get_paginated_response(serializer.data)

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


class MovieOrderCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomIsAuthenticated]
    
    def post(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        user = request.user
        serializer = MovieOrderSerializer(data=request.data, context={"movie": movie, "user": user})

        if not CustomIsAuthenticated().has_permission(request, self):
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if serializer.is_valid():
            movie_order = serializer.save()
            
            response_data = {
                "id": movie_order.id,
                "title": movie_order.movie.title,
                "buyed_at": movie_order.buyed_at,
                "buyed_by": movie_order.user.email,
                "price": movie_order.price,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
