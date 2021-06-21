from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [

    path('employee/register/', views.employee_registration, name='employee-registration'),
    path('employer/register/', views.employer_registration, name='employer-registration'),
    path('profile/edit/<int:id>/', views.employee_edit_profile, name='edit-profile'),
    path('login/', views.user_logIn, name='login'),
    path('logout/', views.user_logOut, name='logout'),

    path('reset_password/', views.reset_password, name="reset_home"),
    path('reset_password/otp/', views.otp_confirmation, name="reset_otp"),
    path('reset_password/change_password/<str:UUID>', views.change_password, name="reset_change"),
]
