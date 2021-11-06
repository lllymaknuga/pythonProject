from django.urls import path

from authentic.views import Registration, Validate

urlpatterns = [
    path('generate/', Registration.as_view()),
    path('validate/', Validate.as_view())
]
