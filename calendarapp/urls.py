from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("insert_event", views.insert_event, name="insert_event"),
    path("event_list", views.event_list, name="event_list"),
    path("event/<int:event_id>/delete", views.event_delete, name="event_delete"),
    path("day_list/<str:date>", views.day_list, name="day_list"),
    path(
        "month_view/<int:year>/<int:month>",
        views.month_view,
        name="month_view",
    ),
]
