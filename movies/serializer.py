from rest_framework import serializers
from movies.models import RatingChoices, Movie, MovieOrder
from users.models import User
       



class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    synopsis = serializers.CharField(
        default=None,
        allow_null=True,
    )
    rating = serializers.ChoiceField(
        choices=RatingChoices.choices, default=RatingChoices.G, allow_null=True
    )
    duration = serializers.CharField(max_length=10, allow_null=True, default=None)
    added_by = serializers.SerializerMethodField()

    def get_added_by(self, obj):
        return obj.user.email

    def create(self, validated_data: dict)-> Movie:
        return Movie.objects.create(**validated_data)



from rest_framework import serializers
from decimal import Decimal

class MovieOrderSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    buyed_by = serializers.SerializerMethodField()
    buyed_at = serializers.ReadOnlyField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2, write_only=True, required=True, coerce_to_string=False)

    def get_title(self, obj):
        return obj.movie.title

    def get_buyed_by(self, obj):
        return obj.user.email

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = "{:.2f}".format(float(data['price']))
        return data

    def create(self, validated_data):
        movie = self.context["movie"]
        user = self.context["user"]
        price = str(validated_data.pop("price"))
        movie_order = MovieOrder.objects.create(movie=movie, user=user, price=price, **validated_data)
        return movie_order

    class Meta:
        model = MovieOrder
        fields = ["id", "title", "price", "buyed_by", "buyed_at"]
