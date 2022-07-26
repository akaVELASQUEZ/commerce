from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:list_id>", views.listing, name="listing"),
    path("listing/<int:list_id>/bid", views.bid, name="bid"),
    path("listing/<int:list_id>/watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:list_id>/comment", views.comment, name="comment"),
    path("watchlist", views.user_watchlist, name="user_watchlist"),
    path("category/<str:category>", views.category, name="category"),
    path("userlisting", views.user_listing, name="user_listing"),
    path("closed", views.closed, name="closed"),
    path("search", views.search, name="search")
]
