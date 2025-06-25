from rest_framework import serializers
from .models import Hotel, FavoriteHotel, Review



class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'



class FavoriteHotelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    hotel_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FavoriteHotel
        fields = ['id', 'user', 'hotel', 'hotel_id']
        read_only_fields = ['id', 'hotel']

    def validate_hotel_id(self, value):
        if not Hotel.objects.filter(id=value).exists():
            raise serializers.ValidationError("Hotel with given id not found")
        return value

    def create(self, validated_data):
        hotel_id = validated_data.pop('hotel_id')
        user = validated_data.pop('user')

        hotel = Hotel.objects.get(id=hotel_id)
        favorite, created = FavoriteHotel.objects.get_or_create(user=user, hotel=hotel)

        if not created:
            raise serializers.ValidationError("This hotel is already in favorites")

        return favorite



class ReviewSerializer(serializers.ModelSerializer):
    hotel_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = [ 'id', 'hotel_id', 'content', 'rating']

    def validate_hotel_id(self, value):
        if not Hotel.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid hotel_id. hotel does not exist.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        hotel = Hotel.objects.get(id=validated_data.pop('hotel_id'))
        user = self.context['request'].user
        existing_review = Review.objects.filter(hotel=hotel, user=user)
        if existing_review.exists():
            raise serializers.ValidationError("you has already reviewed this hotel.")
        
        return Review.objects.create(hotel=hotel, user=user, **validated_data)