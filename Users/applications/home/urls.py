from django.urls import path

from .import views

app_name='home_app'

urlpatterns = [
    path('panel/', views.HomePage.as_view(), name='panel'),
    path('mixin/', views.TemplateTestMixin.as_view(), name='mixin'),
]