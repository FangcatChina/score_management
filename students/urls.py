from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add_score/<int:student_id>/', add_score, name='add_score'),
    path('register/', register, name='register'),
    path('add_student/', add_student, name='add_student'),
    path('score_records/<int:student_id>/', view_score_records, name='view_score_records'),
    path('add_group/', add_group, name='add_group'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student'),
    path('public_ranking/', public_ranking, name='public_ranking'),
    path('update_group_special_score/<int:group_id>/', update_group_special_score, name='update_group_special_score'),
    path('batch_assign_student_to_group/', batch_assign_student_to_group, name='batch_assign_student_to_group'),
    path('batch_add_score/', batch_add_score, name='batch_add_score'),
    path('delete_group/<int:group_id>/', delete_group, name='delete_group'),
    path('search_students/', search_students, name='search_students'),
    path('user_management/', user_management, name='user_management'),
    path('change_user_password/<int:user_id>/', change_user_password, name='change_user_password'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
]