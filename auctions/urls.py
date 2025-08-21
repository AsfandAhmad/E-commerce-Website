from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_Listing, name="create"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addwatchList/<int:id>", views.addWatchList, name="addwatchList"),
    path("removewatchList/<int:id>", views.removeWatchList, name="removewatchList"),
    path("watchList", views.displayWatchList, name="watchList"),
    path("addbit/<int:id>", views.addbit, name="addbit"),
    path("addcomment/<int:id>", views.addcomment, name="addcomment"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),




]
