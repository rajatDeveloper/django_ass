from django.urls import path
from .views import registration_view, custom_auth_token , create_assignment , get_assignments , get_assignment  , get_csrf_token

# , logout_view

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', custom_auth_token, name='login'),
    # path('logout/', logout_view, name='logout'),

    path('create_assignment/', create_assignment, name='create_assignment'),
    path('get_assignments/', get_assignments, name='get_assignments'),
    path('get_assignment/<int:pk>', get_assignment, name='get_assignment'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),

]
