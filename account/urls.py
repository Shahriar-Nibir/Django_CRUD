from django.urls import path
from . import views


urlpatterns = [
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),

    path('', views.home, name='home'),
    path('customer1/<str:pk>', views.customer, name='customer'),
    path('product', views.product, name='product'),

    path('user', views.user, name='user'),
    path('userSettings', views.userSettings, name='userSettings'),

    path('create_order/<str:pk>', views.create_order, name='create_order'),
    path('update_order/<str:pk>', views.update_order, name='update_order'),
    path('delete/<str:pk>', views.delete, name='delete')
]
