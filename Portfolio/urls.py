from django.urls import path
from .views import *

urlpatterns = [
    path('home/',home, name='home'),
    path('registration/',registration, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('contact/', contact, name='contact'),
    path('cv/', cv, name='cv'),
    path('dashboard/', dashboard, name='dashboard'),
    path('update_skill/<int:id>/', update_skill, name='update_skill'),
    path('delete_skill/<int:id>/', delete_skill, name='delete_skill'),
    path('update_experience/<int:id>/', update_experience, name='update_experience'),
    path('delete_experience/<int:id>/', delete_experience, name='delete_experience'),
    path('update_education/<int:id>/', update_education, name='update_education'),
    path('delete_education/<int:id>/', delete_education, name='delete_education'),
    path('update_project/<int:id>/', update_project, name='update_project'),
    path('delete_project/<int:id>/', delete_project, name='delete_project'),
]