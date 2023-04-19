from django.urls import path
from riaapp import views

urlpatterns = [
    path('',views.Home,name="Home"),
    path('signin',views.handleSignin,name="handleSignin"),
    path('login',views.handleLogin,name="handleLogin"),
    path('logout',views.handleLogout,name="handleLogout"), 
    path('logout',views.handleLogout,name="handleLogout"), 
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('request-reset-email',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('enroll',views.handleEnroll,name="handleEnroll"), 
    path('course',views.course,name="course"), 
    path('course',views.course,name="course"), 
    path('attendance',views.attendance,name="attendance"), 
    path('detailsofcourse/<id>',views.handleDetails,name="handleDetails"), 
    path('candidateprofile',views.candidateProfile,name="candidateProfile"), 
    path('candidateupdate/<id>',views.candidateupdate,name="candidateupdate"), 
    path('deletecandidate/<id>',views.deleteCandidate,name="deleteCandidate"), 
]
