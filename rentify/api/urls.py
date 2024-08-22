from django.urls import path
from .auth_views import test_api, signup, signin, update_user, sign_out, delete_user
from .listing_views import get_listings, create_listing, get_listing, get_user, get_user_listings, update_listing, delete_listing


urlpatterns = [
    path("test/",test_api,name="test_server"),
    path('auth/signup',signup,name='signup'),
    path('auth/signin',signin,name='signin'),
    path('auth/signout',sign_out,name='sign_out'),
    path('listing/get', get_listings, name='get_listings'),
    path('listing/create', create_listing,name='create_listing'),
    path('listing/get/<int:id>', get_listing, name='get_listings'),
    path('user/getDetails/<int:id>', get_user, name='get_user_details'),
    path('user/listings/<int:id>', get_user_listings, name='get_user_listings'),
    path('listing/update/<int:id>', update_listing,name='update_listing'),
    path('listing/delete/<int:id>', delete_listing,name='delete_listing'),
    path('user/update/<int:id>', update_user,name='update_user'),
    path('user/delete/<int:id>', delete_user,name='delete_user'),
    
]
