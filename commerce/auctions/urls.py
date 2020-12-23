from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
 


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/create", views.create_listing, name="create_listing"),
    path("listings/watchlist", views.watchlist_items, name="watchlist_items"),
    path("listings/watchlistbutton", views.watchlistbtn, name="watchlistbtn"),
    path("listings/categories", views.categories, name="categories"),
    path("listings/categories/<str:cat>", views.category, name="category"),
    path("listings/<int:list_id>", views.listings, name="listings"),
    path("listings/<int:list_id>/bid", views.newbid, name="newbid"),
    path("listings/<int:list_id>/close", views.close_auction, name="close_auction"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)