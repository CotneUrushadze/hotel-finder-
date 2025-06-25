from rest_framework import filters
from rest_framework import viewsets 
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from rest_framework.exceptions import ValidationError

from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from hotels.models import Hotel, FavoriteHotel, Review
from hotels.pagination import HotelPagination
from hotels.serializers import HotelSerializer, FavoriteHotelSerializer, ReviewSerializer
from hotels.permissions import IsObjectOwnerOrReadOnly, IsDeveloperOrReadOnly


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    pagination_class = HotelPagination 
    permission_classes = [IsDeveloperOrReadOnly]  
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'address', 'description']
    ordering_fields = ['stars']
    ordering = ['name']
    filterset_fields = ['city']

    def get_queryset(self):
        city = self.request.query_params.get('city')
        if not city:
            raise ValidationError({'city': 'You must provide a city like ?city=Paris'})
        return self.queryset.filter(city__iexact=city)

    @swagger_auto_schema(
        operation_description="List hotels in a specific city",
        manual_parameters=[
            openapi.Parameter(
                'city',
                openapi.IN_QUERY,
                description="Choose city",
                type=openapi.TYPE_STRING,
                enum=["paris", "london", "roma", "madrid", "new york"],
                required=True,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    

class FavoriteHotelViewSet(GenericViewSet, 
                           ListModelMixin, 
                           CreateModelMixin, 
                           RetrieveModelMixin, 
                           DestroyModelMixin):
    queryset = FavoriteHotel.objects.all()
    serializer_class = FavoriteHotelSerializer
    permission_classes = [IsAuthenticated]  
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'likes'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    


    

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating']

    def get_queryset(self):
        return self.queryset.filter(hotel_id=self.kwargs['hotel_pk'])