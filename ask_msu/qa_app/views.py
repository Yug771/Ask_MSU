# qa_app/views.py


# PINECONE_API_KEY = 'e2e3f912-2ae4-4ada-8e7c-8575f72e84f3'

# GOOGLE_API_KEY = 'AIzaSyDqrFNYd_A7f6mhQajMN2Qdtpa_eamXlMg'
# -----------------------------------------------------------------------------------------------------------------------
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy  # Import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.views.generic import TemplateView
from .forms import QuestionForm
from .models import Question
from .logic import answer_question  # Import your logic function
from .forms import CustomUserCreationForm
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('qa_app:chatbot') 

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('qa_app:login')  # Use reverse_lazy

def registration_success(request):
    return render(request, 'registration_success.html')


class ChatbotView(FormView):
    template_name = 'chatbot.html'
    form_class = QuestionForm
    success_url = reverse_lazy('qa_app:chatbot')  # Use reverse_lazy

    def form_valid(self, form):
        question_text = form.cleaned_data['question_text']
        answer_text = answer_question(question_text)  # Call your logic function here
        user = self.request.user if self.request.user.is_authenticated else None

        Question.objects.create(user=user, question_text=question_text, answer_text=answer_text)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['questions'] = Question.objects.all()    # Retrieve only the last 3 questions and answers
        context['questions'] = Question.objects.all().order_by('-id')[:1][::-1] # Adjust this query based on your needs
        return context


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('qa_app:registration_success')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
