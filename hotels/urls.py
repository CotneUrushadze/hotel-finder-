from django.urls import path, include
from hotels.views import HotelViewSet, FavoriteHotelViewSet, ReviewViewSet
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('hotels', HotelViewSet)
router.register('favorite-hotels', FavoriteHotelViewSet, basename='favorite-hotels')

urlpatterns = [
    path("", include(router.urls)),
]
hotels_routr = routers.NestedDefaultRouter(
    router,
    'hotels',
    lookup = 'hotel'
)
hotels_routr.register('reviews', ReviewViewSet, basename='hotel-reviews')


urlpatterns = [
    path("", include(router.urls)),
    path("", include(hotels_routr.urls)),  
]