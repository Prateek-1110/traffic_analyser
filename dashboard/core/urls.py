from django.urls import path
from . import views
urlpatterns = [
    path('',          views.home,         name='home'),
    path('map/',      views.map_view,     name='map'),
    path('insights/', views.insights_view,name='insights'),
    path('risk/',     views.risk_view,    name='risk'),
    path('api/predict/', views.predict_api, name='predict_api'),
]