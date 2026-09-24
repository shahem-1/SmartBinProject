from django.contrib import admin
from django.urls import path
from smartbin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.mainP, name='login'),
    path('signup/', views.signup_view, name='Signup'),  
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('api/sensor/', views.sensor_data, name='sensor_data'),
    path('api/sensor/latest/', views.get_sensor_data, name='get_sensor_data'),
    path('api/bins/', views.bin_list_api, name='bin_list_api'),

]
