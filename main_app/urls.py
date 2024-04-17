from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page_view, name="home"),
    path("allMeetingsDataView/", views.allMeetingsData_view, name="allMeetingsData_view"),
    path("fromAllMeetingsData_view/", views.fromAllMeetingsData_view, name="fromAllMeetingsData_view"),
    path("meetingsRatingData_view/", views.meetingsRatingData_view, name="meetingsRatingData_view"),
]
