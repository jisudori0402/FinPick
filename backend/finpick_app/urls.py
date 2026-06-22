from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/diagnosis/', views.api_diagnosis, name='api_diagnosis'),
    path('api/roadmap/', views.api_roadmap, name='api_roadmap'),
    path('api/missions/<int:mission_id>/toggle/', views.api_user_mission, name='api_user_mission'),
    path('api/products/', views.api_products, name='api_products'),
    path('api/deposit-products/', views.api_deposit_products, name='api_deposit_products'),
    path('api/deposit-products/<int:product_id>/', views.api_deposit_product_detail, name='api_deposit_product_detail'),
]
