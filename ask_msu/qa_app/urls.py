# qa_app/urls.py

from django.urls import path
from .views import CustomLoginView, CustomLogoutView, ChatbotView, SignupView, registration_success

app_name = 'qa_app' 

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('chatbot/', ChatbotView.as_view(), name='chatbot'),
    path('registration-success/', registration_success, name='registration_success'),
]
