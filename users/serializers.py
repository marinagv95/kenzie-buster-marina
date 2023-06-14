from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(
        max_length=80,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="username already taken."
            )
        ],
    )
    password = serializers.CharField(max_length=127, write_only=True)
    email = serializers.EmailField(
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="email already registered."
            )
        ],
    )
    birthdate = serializers.DateField(allow_null=True, default=None)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    movies_count = serializers.SerializerMethodField()
    movies_name = serializers.SerializerMethodField

    

    def create(self, validated_data):
        validated_data["is_superuser"] = validated_data.get("is_employee", False)
        user = User.objects.create_user(**validated_data)
        return user
    
    def get_movies_count(self, obj:User):
        return obj.movies.count()
    
    def get_movies_name(self, obj:User):
        movies_title = [movie.title for movie in obj.movies.all()]
        if movies_title:
            return movies_title

        return "sem filmes registrados"    



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=80, write_only=True)
    password = serializers.CharField(max_length=127, write_only=True)