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
    path('api/profile/', views.api_profile, name='api_profile'),
    path('api/community/posts/', views.api_community_posts, name='api_community_posts'),
    path('api/community/posts/<int:post_id>/', views.api_community_post_detail, name='api_community_post_detail'),
    path('api/community/posts/<int:post_id>/comments/', views.api_community_comments, name='api_community_comments'),
    path('api/community/comments/<int:comment_id>/', views.api_community_comment_detail, name='api_community_comment_detail'),
    path('api/deposit-products/', views.api_deposit_products, name='api_deposit_products'),
    path('api/deposit-products/<int:product_id>/', views.api_deposit_product_detail, name='api_deposit_product_detail'),
    path('api/deposit-products/<int:product_id>/join/', views.api_join_deposit_product, name='api_join_deposit_product'),
    path('api/deposit-products/<int:product_id>/favorite/', views.api_favorite_deposit_product_toggle, name='api_favorite_deposit_product_toggle'),
    path('api/favorite-deposit-products/', views.api_favorite_deposit_products, name='api_favorite_deposit_products'),
    path('api/bank-route/', views.api_bank_route, name='api_bank_route'),
    path('api/spot-prices/', views.api_spot_prices, name='api_spot_prices'),
]
