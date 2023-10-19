from django.urls import re_path, path
from . import views
from .views import JustifyTextView

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),
    re_path('justify/', JustifyTextView.as_view(),name="justify-text")
    #re_path('justify/', views.justify_text),

]
