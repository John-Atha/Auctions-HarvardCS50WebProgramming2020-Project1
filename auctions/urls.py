from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcomepage, name="in"),
    path("active", views.index, name="index"),
    path("inactive", views.inactive, name="inactive"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add", views.add, name="add"),
    path("listing:<str:name>", views.display, name="display"),
    path("category:<title>", views.cat_display, name="cat_display"),
    path("addwatchlist:<name>", views.watch, name="watch"),
    path("removewatchlist:<name>", views.unwatch, name="unwatch"),
    path("deactivate:<name>", views.deactivate, name="deactivate")
]